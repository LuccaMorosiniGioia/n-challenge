import openai
from openai import OpenAI
from typing import Dict, Any, Tuple

from ..config.settings import Settings
from dotenv import load_dotenv

load_dotenv()


class SqlService:
    def __init__(self):
        self.settings = Settings()
        openai.api_key = self.settings.OPENAI_API_KEY
        self.model = self.settings.OPENAI_MODEL
        self.temperature = 0
        self.client = OpenAI(api_key=self.settings.OPENAI_API_KEY)
        self.messages = self.settings.BASE_SQL_MESSAGES

    def __append_to_msgs__(self, message: str, role: str) -> None:
        msg_dict = {"role": role, "content": message}
        self.messages.append(msg_dict)

    def process_message(self, message: str) -> str:
        self.__append_to_msgs__(message, "user")

        try:
            response = self.__send_completion_msg__()
            return response.choices[0].message.content

        except Exception as e:
            print(f"Error processing message: {e}")
            return "Sorry, I encountered an error processing your message."

    def __append_to_msgs__(self, message: str, role: str) -> None:
        msg_dict = {"role": role, "content": message}
        self.messages.append(msg_dict)

    def __send_completion_msg__(self):
        ret = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=self.temperature,
        )

        return ret
