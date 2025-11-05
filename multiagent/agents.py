from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, List, Optional, Sequence

from .llm_client import LLMClient, LLMResult
from .logging_utils import get_logger

Message = dict[str, str]


@dataclass(frozen=True)
class AgentOutput:
    agent_name: str
    role: str
    content: str
    reasoning: List[str]
    raw: Any


class Agent:
    def __init__(self, name: str, role: str, system_prompt: str, llm: LLMClient) -> None:
        self.name = name
        self.role = role
        self._system_prompt = system_prompt.strip()
        self._llm = llm
        self._logger = get_logger(f"multiagent.agent.{name.lower().replace(' ', '_')}")

    def run(self, prompt: str, memory: Optional[Sequence[Message]] = None) -> AgentOutput:
        messages: List[Message] = [{"role": "system", "content": self._system_prompt}]
        if memory:
            messages.extend(memory)
        messages.append({"role": "user", "content": prompt})

        self._logger.info("Executing agent '%s' with prompt length=%d", self.name, len(prompt))
        result: LLMResult = self._llm.chat(messages)
        self._logger.info("Agent '%s' completed", self.name)

        return AgentOutput(
            agent_name=self.name,
            role=self.role,
            content=result.content,
            reasoning=result.reasoning,
            raw=result.raw,
        )


class PlannerAgent(Agent):
    def __init__(self, llm: LLMClient) -> None:
        super().__init__(
            name="Strategic Planner",
            role="Planning Maestro",
            system_prompt="""
You are the Strategic Planner in a high-stakes innovation task force.
Break down ambitious objectives into phased, achievable missions.
Craft clear deliverables, success metrics, and dependencies for each phase.
Always output Markdown with the following structure:

# Strategic Execution Plan
- **Mission Objective:** <concise paraphrase>

## Guiding Principles
- principle bullets

## Milestones
1. <milestone name>
   - Purpose: ...
   - Activities: ...
   - Deliverables: ...
   - Success Criteria: ...

## Risk Radar
- Risk: ... | Mitigation: ...
""",
            llm=llm,
        )


class ResearchAgent(Agent):
    def __init__(self, llm: LLMClient) -> None:
        super().__init__(
            name="Insight Researcher",
            role="Domain Expert",
            system_prompt="""
You are the Insight Researcher aggregating multi-disciplinary knowledge.
For each milestone, surface cutting-edge research, case studies, and quantitative signals.
Prioritize actionable insights and cite key data points when available.
Output Markdown using this structure:

# Insight Report
- **Plan Synopsis:** <one sentence>

## Deep Dives
### <Milestone Name>
- Evidence: ...
- Signals & Benchmarks: ...
- Open Questions: ...

## Knowledge Gaps
- Gap: ... | Path to close: ...
""",
            llm=llm,
        )


class EngineeringAgent(Agent):
    def __init__(self, llm: LLMClient) -> None:
        super().__init__(
            name="Solution Engineer",
            role="Architect & Implementer",
            system_prompt="""
You are the Solution Engineer translating strategy and research into actionable systems.
Synthesize architecture, processes, and implementation blueprints.
Where algorithms or data flows are required, provide concrete steps.
Respond in Markdown using this template:

# Execution Blueprint
- **Mission Context:** <summary>

## System Architecture
- Components and responsibilities
- Data contracts or APIs

## Implementation Plan
1. Step ...
2. Step ...

## Resource Matrix
- Role: ... | Skills: ... | Allocation: ...

## Quality & Measurement
- KPI: ... | Definition: ... | Measurement cadence: ...
""",
            llm=llm,
        )


class ReviewerAgent(Agent):
    def __init__(self, llm: LLMClient) -> None:
        super().__init__(
            name="Critical Reviewer",
            role="Risk & Quality Analyst",
            system_prompt="""
You are the Critical Reviewer ensuring the multi-agent proposal is robust.
Stress-test the plan, insights, and blueprint for feasibility, coherence, and blind spots.
Highlight contradictions and recommend high-leverage refinements.
Respond in Markdown using this format:

# Executive Assessment

## Strengths Snapshot
- ...

## Critical Risks
- Risk: ... | Severity: ... | Recommended Action: ...

## Alignment Check
- Observation: ... | Impact: ... | Adjustment: ...

## Final Verdict
- Confidence Level: <High/Medium/Low>
- Next Critical Decision: ...
""",
            llm=llm,
        )
