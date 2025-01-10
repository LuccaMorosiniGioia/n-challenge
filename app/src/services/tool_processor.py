from .database_service import DatabaseService
from .sql_service import SqlService
from .plot_service import PlotService


class ToolProcessor:
    def __init__(
        self,
        tool_function_name: str,
    ) -> None:
        self.tool_function_name = tool_function_name
        self.sql_service = SqlService()
        self.graph_service = PlotService()
        self.database_service = DatabaseService()

    def __create_query__(self, tool_args: dict) -> str:
        question = tool_args.get("question")
        if question is None:
            raise ValueError("Error: question is required")

        complete_question = (
            "Generate a SQL Query to answer the following question: " + question
        )

        try:
            sql_query = (
                self.sql_service.process_message(complete_question)
                .strip("***")
                .strip("'''")
                .strip("```")
            )  # Sometimes the response comes with these characters
        except Exception as e:
            print(f"Error processing message on sql service: {e}")
            raise RuntimeError(f"{e}")

        print("\nSQL QUERY: ")
        print(sql_query)

        try:
            response_df = self.database_service.query_db(sql_query)
        except Exception as e:
            print(f"Error processing query on database service: {e}")
            raise RuntimeError(f"{e}")

        complete_question = (
            "# Chose the best plot to fit this Dataset: "
            + response_df.to_json()
            + "\n# Consider that the asked questions was: "
            + question
        )
        try:
            plots = self.graph_service.process_message(complete_question)
        except Exception as e:
            print(f"Error processing message on plot service: {e}")
            plots = []

        return response_df.to_json(), plots

    def process(self, tool_args):
        processor_map = {
            "create_query": self.__create_query__,
        }

        function = processor_map.get(self.tool_function_name)
        if function is None:
            print(f"Error: tool {self.tool_function_name} does not exist")
            raise TypeError(f"Error: tool {self.tool_function_name} does not exist")

        try:
            return function(tool_args)
        except Exception as e:
            print(f"Error on ToolProcessor: {e}")
            raise RuntimeError(f"{e}")
