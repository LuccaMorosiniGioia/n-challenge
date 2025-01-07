import openai
from openai import OpenAI
from typing import Dict, Any, Tuple
import json
import asyncio

from .tool_processor import ToolProcessor
from ..config.settings import Settings
from .database_service import DatabaseService
from ..tools.create_query_tool import create_query_tool


from dotenv import load_dotenv

load_dotenv()


class OpenAIService:
    def __init__(self, sql_query_creator_agent=False):
        settings = Settings()
        openai.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.temperature = settings.TEMPERATURE
        self.client = OpenAI()
        self.tools = [create_query_tool]
        self.sql_query_creator_agent = sql_query_creator_agent

        if sql_query_creator_agent:
            self.messages = settings.BASE_SQL_MESSAGES
        else:
            self.messages = settings.BASE_MESSAGES


    def process_message(self, message: str) -> str:
        self.__append_to_msgs__(message, "user")

        try:
            response = self.__send_completion_msg__()

            completion = response.choices[0].message
            return self.__process_tools__(completion)

        except Exception as e:
            print(f"Error processing message: {e}")
            return "Sorry, I encountered an error processing your message."

    def __append_to_msgs__(self, message: str, role: str) -> None:
        msg_dict = {"role": role, "content": message}
        self.messages.append(msg_dict)

    def __send_completion_msg__(self):

        if self.sql_query_creator_agent:
            tool_choice = "none"
        else:
            tool_choice = "auto"

        ret = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=self.tools,
            tool_choice=tool_choice,
            temperature=self.temperature,
        )

        return ret

    def __process_tools__(self, response_message: Dict[str, str]) -> str:
        tool_calls = getattr(response_message, "tool_calls", None)
        if not tool_calls:
            return response_message.content

        self.messages.append(response_message)
        for tool_call in tool_calls:
            tool_call_id = tool_call.id
            tool_function_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            print("tool name:", tool_function_name)
            print(tool_args)

            results = ToolProcessor(
                tool_function_name=tool_function_name,
            ).process(tool_args)

            self.messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "name": tool_function_name,
                    "content": results,
                }
            )

        response = self.__send_completion_msg__()
        return response.choices[0].message.content
