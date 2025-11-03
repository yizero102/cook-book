"""Higher level orchestration that mimics a simplified assistant."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, Mapping, MutableMapping, Sequence

from .llm_client import AnthropicClient, AnthropicError

DEFAULT_SYSTEM_PROMPT = (
    "You are a careful software engineering assistant operating in a constrained "
    "environment. Provide clear, structured, and reproducible answers."
)


class ToolRegistrationError(ValueError):
    """Raised when attempting to register an invalid tool specification."""


class ToolExecutionError(RuntimeError):
    """Raised when a registered tool fails."""


@dataclass
class ToolSpec:
    name: str
    description: str
    handler: Callable[..., Any]
    input_schema: Mapping[str, Any] | None = None

    def to_anthropic_descriptor(self) -> Mapping[str, Any]:
        schema = self.input_schema or {"type": "object", "properties": {}, "additionalProperties": True}
        return {
            "name": self.name,
            "description": self.description,
            "input_schema": schema,
        }


@dataclass(frozen=True)
class CapabilityReport:
    requested: tuple[str, ...]
    available: tuple[str, ...]
    missing: tuple[str, ...]
    notes: Mapping[str, str] = field(default_factory=dict)

    def is_full_match(self) -> bool:
        return not self.missing


_DEFAULT_EXPECTATIONS: Dict[str, str] = {
    "multi_turn_conversation": "Maintains conversation history across turns.",
    "tool_usage": "Allows registering and invoking Python callables as tools.",
    "self_diagnostics": "Can report on its own configured capabilities.",
    "llm_connectivity": "Has an LLM client attached for generating responses.",
}


class AssistantReplica:
    """Facade combining conversation state management and tool orchestration."""

    def __init__(
        self,
        llm_client: AnthropicClient,
        *,
        system_prompt: str | None = None,
    ) -> None:
        self.llm = llm_client
        self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
        self._history: list[dict[str, Any]] = []
        self._tools: MutableMapping[str, ToolSpec] = {}
        if self.system_prompt:
            self._history.append(self._as_message("system", self.system_prompt))

    def reset(self) -> None:
        self._history = []
        if self.system_prompt:
            self._history.append(self._as_message("system", self.system_prompt))

    def set_system_prompt(self, prompt: str) -> None:
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("System prompt must be a non-empty string.")
        self.system_prompt = prompt
        self.reset()

    def register_tool(
        self,
        name: str,
        handler: Callable[..., Any],
        *,
        description: str,
        input_schema: Mapping[str, Any] | None = None,
    ) -> None:
        if name in self._tools:
            raise ToolRegistrationError(f"Tool '{name}' already registered.")
        if not callable(handler):
            raise ToolRegistrationError("Tool handler must be callable.")
        if not description:
            raise ToolRegistrationError("Tool description cannot be empty.")
        spec = ToolSpec(name=name, description=description, handler=handler, input_schema=input_schema)
        self._tools[name] = spec

    def invoke_tool(self, name: str, /, **kwargs: Any) -> Any:
        if name not in self._tools:
            raise ToolExecutionError(f"Tool '{name}' is not registered.")
        handler = self._tools[name].handler
        try:
            return handler(**kwargs)
        except TypeError as exc:
            raise ToolExecutionError(f"Invalid parameters for tool '{name}': {exc}") from exc
        except Exception as exc:  # pragma: no cover - defensive
            raise ToolExecutionError(f"Tool '{name}' raised an unexpected error: {exc}") from exc

    def ask(
        self,
        prompt: str,
        *,
        max_output_tokens: int = 512,
        temperature: float | None = None,
    ) -> str:
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt must be a non-empty string.")
        user_message = self._as_message("user", prompt)
        conversation = [*self._history, user_message]
        tools = [spec.to_anthropic_descriptor() for spec in self._tools.values()]
        response = self.llm.create_message(
            conversation,
            max_output_tokens=max_output_tokens,
            temperature=temperature,
            tools=tools if tools else None,
        )
        text = self.llm.extract_text(response)
        assistant_message = self._as_message("assistant", text)
        self._history.extend([user_message, assistant_message])
        return text

    def available_capabilities(self) -> tuple[str, ...]:
        capabilities = ["multi_turn_conversation", "self_diagnostics", "llm_connectivity"]
        if self._tools:
            capabilities.append("tool_usage")
        else:
            # Tool registration is supported even if no tools present yet.
            capabilities.append("tool_registry")
        return tuple(dict.fromkeys(capabilities))

    def assess_parity(self, reference: Sequence[str] | None = None) -> CapabilityReport:
        baseline = tuple(reference) if reference is not None else tuple(_DEFAULT_EXPECTATIONS.keys())
        available = set(self.available_capabilities())
        missing: list[str] = []
        notes: Dict[str, str] = {}
        for capability in baseline:
            if capability not in available:
                missing.append(capability)
                notes[capability] = _DEFAULT_EXPECTATIONS.get(capability, "Missing capability.")
        return CapabilityReport(
            requested=baseline,
            available=tuple(sorted(available)),
            missing=tuple(sorted(missing)),
            notes=notes,
        )

    def describe(self) -> str:
        report = self.assess_parity()
        lines = ["Assistant Replica Capability Report:"]
        lines.append(f"- Connected to LLM: {'yes' if 'llm_connectivity' in report.available else 'no'}")
        lines.append(f"- Registered tools: {len(self._tools)}")
        if report.missing:
            lines.append("- Missing capabilities: " + ", ".join(report.missing))
        else:
            lines.append("- All expected capabilities are available.")
        return "\n".join(lines)

    def conversation_history(self) -> tuple[Mapping[str, Any], ...]:
        return tuple(self._history)

    @staticmethod
    def _as_message(role: str, text: str) -> dict[str, Any]:
        return {
            "role": role,
            "content": [
                {
                    "type": "text",
                    "text": text,
                }
            ],
        }
