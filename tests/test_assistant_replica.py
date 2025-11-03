from __future__ import annotations

import unittest

from assistant_clone.assistant import AssistantReplica, ToolExecutionError, ToolRegistrationError


class StubLLM:
    def __init__(self) -> None:
        self.calls = []

    def create_message(self, messages, **kwargs):
        messages = list(messages)
        self.calls.append({"messages": messages, "kwargs": kwargs})
        last_user = next(
            (msg for msg in reversed(messages) if msg["role"] == "user"),
            {"content": [{"text": "", "type": "text"}]},
        )
        text = last_user["content"][0]["text"]
        return {"content": [{"type": "text", "text": f"echo:{text}"}]}

    @staticmethod
    def extract_text(response):
        return response["content"][0]["text"]


class AssistantReplicaTests(unittest.TestCase):
    def test_conversation_flow(self) -> None:
        llm = StubLLM()
        assistant = AssistantReplica(llm_client=llm)
        reply = assistant.ask("Hello there")
        self.assertEqual(reply, "echo:Hello there")
        history = assistant.conversation_history()
        self.assertGreaterEqual(len(history), 3)  # system, user, assistant
        self.assertEqual(history[-1]["role"], "assistant")

    def test_tool_registration_and_execution(self) -> None:
        llm = StubLLM()
        assistant = AssistantReplica(llm_client=llm)

        def add_numbers(a: int, b: int) -> int:
            return a + b

        assistant.register_tool("add", add_numbers, description="Adds numbers")
        result = assistant.invoke_tool("add", a=2, b=3)
        self.assertEqual(result, 5)
        report = assistant.assess_parity(["tool_usage"])
        self.assertFalse(report.missing)

    def test_tool_registration_validation(self) -> None:
        llm = StubLLM()
        assistant = AssistantReplica(llm_client=llm)
        assistant.register_tool("noop", lambda: None, description="Nothing")
        with self.assertRaises(ToolRegistrationError):
            assistant.register_tool("noop", lambda: None, description="Duplicate")
        with self.assertRaises(ToolExecutionError):
            assistant.invoke_tool("missing")

    def test_capability_report_missing_tool_usage(self) -> None:
        llm = StubLLM()
        assistant = AssistantReplica(llm_client=llm)
        report = assistant.assess_parity()
        self.assertIn("tool_usage", report.missing)

    def test_describe_mentions_missing_capabilities(self) -> None:
        llm = StubLLM()
        assistant = AssistantReplica(llm_client=llm)
        summary = assistant.describe()
        self.assertIn("Missing capabilities", summary)


if __name__ == "__main__":
    unittest.main()
