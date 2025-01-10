import openai
from openai import OpenAI
from typing import Dict, Any, Tuple
import json
import re

from .tool_processor import ToolProcessor
from ..tools.create_query_tool import create_query_tool
from ..config.settings import Settings
from dotenv import load_dotenv

load_dotenv()


class ChatService:
    def __init__(self):
        self.settings = Settings()
        openai.api_key = self.settings.OPENAI_API_KEY
        self.model = self.settings.OPENAI_MODEL
        self.temperature = self.settings.TEMPERATURE
        self.client = OpenAI()
        self.tools = [create_query_tool]
        self.messages = self.settings.BASE_MESSAGES

    def __append_to_msgs__(self, message: str, role: str) -> None:
        msg_dict = {"role": role, "content": message}
        self.messages.append(msg_dict)

    def process_message(self, message: str) -> str:
        self.__append_to_msgs__(message, "user")

        try:
            response = self.__send_completion_msg__()

            return self.__process_tools__(response.choices[0].message)

        except Exception as e:
            print(f"Error processing message: {e}")
            return "Sorry, I encountered an error processing your message.", None, []

    def __append_to_msgs__(self, message: str, role: str) -> None:
        msg_dict = {"role": role, "content": message}
        self.messages.append(msg_dict)

    def __send_completion_msg__(self):
        ret = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=self.tools,
            tool_choice="auto",
            temperature=self.temperature,
        )

        return ret

    def __match_regex__(self, text, match) -> str:
        # Regex para extrair o texto entre as tags <match> e </match>
        regex = rf"<{match}>\s*(.*?)\s*</{match}>"
        # Usando re.search para encontrar o texto
        match = re.search(regex, text, re.DOTALL)
        if match:
            response = match.group(1).strip()
        else:
            response = ""

        return response

    def __process_reasoning__(self, response: str, arr_plots=[]) -> str:
        response = response.strip("```")

        cont_response = self.__match_regex__(response, "contemplator").replace("#", "")
        ans_response = self.__match_regex__(response, "final_answer").replace("#", "")

        # print("Response: ")
        # print(response)

        # print("Comtemplation: ")
        # print(cont_response)

        # print("\nFinal Answer: ")
        # print(ans_response)

        return cont_response, ans_response, arr_plots

    def __process_tools__(self, response_message: Dict[str, str]) -> str:
        tool_calls = getattr(response_message, "tool_calls", None)
        if not tool_calls:
            return response_message.content, None, []

        self.messages.insert(2, self.settings.REASONING_MESSAGE)

        arr_plots = []
        self.messages.append(response_message)
        for tool_call in tool_calls:
            tool_call_id = tool_call.id
            tool_function_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            print("tool name:", tool_function_name)
            print(tool_args)

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

        response = self.__send_completion_msg__()
        return self.__process_reasoning__(
            response.choices[0].message.content, arr_plots
        )
