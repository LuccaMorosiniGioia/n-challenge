from abc import ABC, abstractmethod
import datetime as dt


class BaseProcessor(ABC):
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def process(self, tool_args, orgid: int):
        pass
