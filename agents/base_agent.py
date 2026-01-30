from abc import ABC, abstractmethod
from loguru import logger

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        logger.info(f"Agent initialized: {self.name}")

    @abstractmethod
    def run(self, *args, **kwargs):
        pass

    def validate(self, data):
        if data is None:
            raise ValueError(f"{self.name}: Received empty data")
        return True
