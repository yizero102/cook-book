from abc import ABC, abstractmethod
from multi_agent_system.llm.llm_client import LLMClient

class BaseAgent(ABC):
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.llm_client = LLMClient()

    @abstractmethod
    def execute_task(self, task: str):
        pass

    def _invoke_llm(self, messages):
        return self.llm_client.invoke(messages)
