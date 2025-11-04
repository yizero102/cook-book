"""Public interface for the local assistant package."""

from .assistant import AssistantConfig, LocalAssistant
from .llm_client import LLMClient, LLMClientConfig, LLMError

__all__ = [
    "AssistantConfig",
    "LocalAssistant",
    "LLMClient",
    "LLMClientConfig",
    "LLMError",
]
