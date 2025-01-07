import pandas as pd
from .base_processor import BaseProcessor


class CreateQuery(BaseProcessor):
    def __init__(self, **kwargs):
        pass

    def process(self, tool_args: dict) -> str:
        question = tool_args["question"]

        results = pd.DataFrame()

        return results.to_json()
