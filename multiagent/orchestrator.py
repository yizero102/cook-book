from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .agents import (
    AgentOutput,
    EngineeringAgent,
    PlannerAgent,
    ResearchAgent,
    ReviewerAgent,
)
from .config import LLMConfig, load_llm_config
from .llm_client import LLMClient
from .logging_utils import get_logger


@dataclass(frozen=True)
class OrchestrationResult:
    objective: str
    context: Optional[str]
    plan: AgentOutput
    insights: AgentOutput
    blueprint: AgentOutput
    assessment: AgentOutput

    def to_markdown(self) -> str:
        sections = [
            f"# Mission Objective\n{self.objective}\n",
        ]
        if self.context:
            sections.append(f"## Context\n{self.context}\n")

        sections.extend([
            f"## Strategic Plan\n{self.plan.content}\n",
            f"## Insight Synthesis\n{self.insights.content}\n",
            f"## Execution Blueprint\n{self.blueprint.content}\n",
            f"## Executive Assessment\n{self.assessment.content}\n",
        ])
        return "\n".join(sections)


class MultiAgentOrchestrator:
    def __init__(self, config: Optional[LLMConfig] = None) -> None:
        self._logger = get_logger("multiagent.orchestrator")
        llm_config = config or load_llm_config()
        self._llm = LLMClient(llm_config)

        self._planner = PlannerAgent(self._llm)
        self._researcher = ResearchAgent(self._llm)
        self._engineer = EngineeringAgent(self._llm)
        self._reviewer = ReviewerAgent(self._llm)

    def run_workflow(self, mission: str, context: Optional[str] = None) -> OrchestrationResult:
        context_block = f"\nContext: {context}" if context else ""

        planner_prompt = (
            "You must design an actionable, phased delivery plan for the mission below.\n"
            "Be ambitious yet realistic, detail deliverables and risks for each phase.\n\n"
            f"Mission: {mission}{context_block}\n"
        )
        plan_output = self._planner.run(planner_prompt)

        research_memory = [
            {"role": "user", "content": f"Mission: {mission}"},
            {"role": "assistant", "name": self._planner.name, "content": plan_output.content},
        ]
        research_prompt = (
            "Interrogate the strategic plan above. Aggregate the strongest evidence, benchmarks, and insights "
            "for each milestone so the implementation team has authoritative guidance."
        )
        insight_output = self._researcher.run(research_prompt, memory=research_memory)

        engineer_memory = [
            {"role": "user", "content": f"Mission: {mission}"},
            {"role": "assistant", "name": self._planner.name, "content": plan_output.content},
            {"role": "assistant", "name": self._researcher.name, "content": insight_output.content},
        ]
        engineer_prompt = (
            "Transform the strategy and insights above into a rigorous execution program. "
            "Specify system components, collaboration models, and verification tactics."
        )
        blueprint_output = self._engineer.run(engineer_prompt, memory=engineer_memory)

        reviewer_memory = [
            {"role": "user", "content": f"Mission: {mission}"},
            {"role": "assistant", "name": self._planner.name, "content": plan_output.content},
            {"role": "assistant", "name": self._researcher.name, "content": insight_output.content},
            {"role": "assistant", "name": self._engineer.name, "content": blueprint_output.content},
        ]
        reviewer_prompt = (
            "Evaluate the plan, insights, and blueprint for coherence and risk. "
            "Identify fatal flaws, material risks, and propose decisive next steps."
        )
        assessment_output = self._reviewer.run(reviewer_prompt, memory=reviewer_memory)

        self._logger.info("Workflow completed for mission: %s", mission)
        return OrchestrationResult(
            objective=mission,
            context=context,
            plan=plan_output,
            insights=insight_output,
            blueprint=blueprint_output,
            assessment=assessment_output,
        )


def run_default_workflow(mission: str, context: Optional[str] = None) -> OrchestrationResult:
    orchestrator = MultiAgentOrchestrator()
    return orchestrator.run_workflow(mission=mission, context=context)
