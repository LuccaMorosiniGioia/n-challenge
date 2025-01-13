import openai
from openai import OpenAI
from typing import Dict, Any, Tuple
import json
import re

from .tool_processor import ToolProcessor
from ..tools.create_query_tool import create_query_tool
from ..config.settings import Settings
from .database_service import DatabaseService
from dotenv import load_dotenv

load_dotenv()


class ChatService:
    def __init__(self):
        self.settings = Settings()
        openai.api_key = self.settings.OPENAI_API_KEY
        self.model = self.settings.OPENAI_MODEL
        self.temperature = self.settings.TEMPERATURE
        self.client = OpenAI(api_key=self.settings.OPENAI_API_KEY)
        self.tools = [create_query_tool]
        # All initial prompts are located in the settings file
        self.base_messages = self.settings.BASE_MESSAGES
        self.messages = []
        self.history_messages = []
        self.database_service = DatabaseService()

    def __append_to_msgs__(self, message: str, role: str) -> None:
        msg_dict = {"role": role, "content": message}
        self.messages.append(msg_dict)
        self.history_messages.append(msg_dict)

    def process_message(self, message: str) -> str:
        # Starting point for the chatbot. For each call we would receive the message and the user that sent it. The first thing to do is retrive the message history from the database.
        # For now we are considering all users to have the same username. In production the key to retrive message history would be a unique identifier not the username.
        self.messages = self.database_service.get_conversations("user_test")

        self.__append_to_msgs__(message, "user")
        try:
            response = self.__send_completion_msg__()

            # We send the users message and in __process_tools__ we check and process any tools that may be called
            return self.__process_tools__(response.choices[0].message)

        except Exception as e:
            print(f"Error processing message: {e}")
            return "Sorry, I encountered an error processing your message.", None, []

    def __send_completion_msg__(self):
        ret = self.client.chat.completions.create(
            model=self.model,
            messages=self.base_messages + self.messages,
            tools=self.tools,
            tool_choice="auto",
            temperature=self.temperature,
        )

        return ret

    def __match_regex__(self, text, match) -> str:
        # Regex para extrair o texto entre as tags <match> e </match>
        regex = rf"<{match}>\s*(.*?)\s*</{match}>"

        match = re.search(regex, text, re.DOTALL)
        if match:
            response = match.group(1).strip()
        else:
            response = ""

        return response

    def __save_history__(self) -> None:
        # We are considering all users to have the same username for now. In production it would be the user's username from the current session
        msgs = [
            {"role": msg["role"], "username": "user_test", "message": msg["content"]}
            for msg in self.history_messages
        ]
        self.database_service.save_conversation(msgs)

    def __process_reasoning__(self, response: str, arr_plots=[]) -> str:
        # All answer come with two block: contemplation(reasoning) and final answer. We extract them to format if needed on the front
        response = response.strip("```")
        self.__append_to_msgs__(response, "assistant")

        # Extract blocks using regex
        cont_response = self.__match_regex__(response, "contemplator").replace("#", "")
        ans_response = self.__match_regex__(response, "final_answer").replace("#", "")

        # print("Response: ")
        # print(response)

        # print("Comtemplation: ")
        # print(cont_response)

        # print("\nFinal Answer: ")
        # print(ans_response)

        self.__save_history__()

        return cont_response, ans_response, arr_plots

    def __process_tools__(self, response_message: Dict[str, str]) -> str:
        tool_calls = getattr(response_message, "tool_calls", None)

        # If there are no tool calls we just append the response to the messages and save the history and return the models answer
        if not tool_calls:
            self.__append_to_msgs__(response_message.content, role="assistant")
            self.__save_history__()
            return response_message.content, None, []

        # We only add the deep reasoning prompt if we need to understand and process a database query
        self.base_messages.append(self.settings.REASONING_MESSAGE)
        arr_plots = []
        self.messages.append(response_message)
        for tool_call in tool_calls:
            tool_call_id = tool_call.id
            tool_function_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            print("tool name:", tool_function_name)
            print(tool_args)

            # For each tool that was called (could be many) we let ToolProcessor handle it. It will return (in this case) the database query result and correspondings plots
            results, plots = ToolProcessor(
                tool_function_name=tool_function_name,
            ).process(tool_args)
            arr_plots.append(plots)

            self.messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "name": tool_function_name,
                    "content": results,
                }
            )

        # we send to the model all the tool results and receive the data analysis which is parsed in __process_reasoning__
        response = self.__send_completion_msg__()
        return self.__process_reasoning__(
            response.choices[0].message.content, arr_plots
        )
