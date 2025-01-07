from openai import OpenAI

from ..config.settings import Settings
from .database_service import DatabaseService
from .openai_service import OpenAIService


class ToolProcessor:
    def __init__(
        self,
        tool_function_name: str,
    ) -> None:
        self.tool_function_name = tool_function_name
        self.openai_service = OpenAIService(sql_query_creator_agent=True)
        self.database_service = DatabaseService()

    def __create_query__(self, tool_args: dict) -> str:
        question = tool_args.get("question")
        if question is None:
            raise ValueError("Error: question is required")

        question = "Generate a SQL Query to answer the following question: " + question
        
        ret = self.openai_service.process_message(question)
        print("Query: ", ret)
        return ret

    def process(self, tool_args):
        processor_map = {
            "create_query": self.__create_query__,
        }

        function = processor_map.get(self.tool_function_name)
        if function is None:
            print(f"Error: tool {self.tool_function_name} does not exist")
            raise TypeError(f"Error: tool {self.tool_function_name} does not exist")

        try:
            return function(
                tool_args
            )
        except Exception as e:
            print(f"Error on ToolProcessor: {e}")
            raise RuntimeError(f"{e}")
