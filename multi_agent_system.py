"""
Multi-Agent System Orchestrator
Coordinates multiple agents to solve complex problems.
"""

import json
from typing import Any, Dict, List, Optional

from agents import (
    AnalystAgent,
    CoordinatorAgent,
    CriticAgent,
    ProblemSolverAgent,
    ResearchAgent,
    SynthesizerAgent,
)
from llm_client import LLMClient


class MultiAgentSystem:
    """
    Orchestrates a team of specialized agents to solve complex problems.
    """
    
    def __init__(self, llm_client: LLMClient):
        """Initialize the multi-agent system."""
        self.llm_client = llm_client
        
        # Initialize all agents
        self.coordinator = CoordinatorAgent(llm_client)
        self.researcher = ResearchAgent(llm_client)
        self.analyst = AnalystAgent(llm_client)
        self.problem_solver = ProblemSolverAgent(llm_client)
        self.critic = CriticAgent(llm_client)
        self.synthesizer = SynthesizerAgent(llm_client)
        
        self.agents = {
            "coordinator": self.coordinator,
            "researcher": self.researcher,
            "analyst": self.analyst,
            "problem_solver": self.problem_solver,
            "critic": self.critic,
            "synthesizer": self.synthesizer,
        }
        
        self.execution_history: List[Dict[str, Any]] = []
    
    def solve(self, problem: str, max_iterations: int = 10) -> Dict[str, Any]:
        """
        Solve a complex problem using the multi-agent system.
        
        Args:
            problem: The problem statement
            max_iterations: Maximum number of agent interactions
            
        Returns:
            Dictionary with the solution and execution history
        """
        print(f"\n{'='*80}")
        print(f"MULTI-AGENT SYSTEM: Starting problem-solving process")
        print(f"{'='*80}")
        print(f"Problem: {problem}\n")
        
        # Step 1: Coordinator plans the approach
        print("Step 1: Coordinator planning approach...")
        planning_response = self.coordinator.think(
            f"""Analyze this problem and create a plan:

Problem: {problem}

Create a detailed plan that specifies:
1. What subtasks need to be done
2. Which agents should handle each subtask
3. The order of execution
4. Expected outcomes

Provide your plan in a clear, structured format.""",
            metadata={"phase": "planning", "problem": problem}
        )
        
        self._record_execution("coordinator", "planning", planning_response)
        print(f"Plan created: {planning_response['content'][:200]}...\n")
        
        # Step 2: Research phase
        print("Step 2: Research phase...")
        research_response = self.researcher.think(
            f"""Research this problem thoroughly:

Problem: {problem}

Coordinator's plan:
{planning_response['content']}

Provide comprehensive research findings including:
- Key concepts and definitions
- Relevant background information
- Important considerations
- Potential challenges""",
            metadata={"phase": "research", "problem": problem}
        )
        
        self._record_execution("researcher", "research", research_response)
        print(f"Research completed: {research_response['content'][:200]}...\n")
        
        # Step 3: Analysis phase
        print("Step 3: Analysis phase...")
        analysis_response = self.analyst.think(
            f"""Analyze the research findings for this problem:

Problem: {problem}

Research findings:
{research_response['content']}

Provide analysis including:
- Key patterns and insights
- Critical factors
- Constraints and requirements
- Risk assessment""",
            metadata={"phase": "analysis", "problem": problem}
        )
        
        self._record_execution("analyst", "analysis", analysis_response)
        print(f"Analysis completed: {analysis_response['content'][:200]}...\n")
        
        # Step 4: Problem-solving phase
        print("Step 4: Problem-solving phase...")
        solution_response = self.problem_solver.think(
            f"""Design a solution for this problem:

Problem: {problem}

Research findings:
{research_response['content'][:500]}...

Analysis:
{analysis_response['content'][:500]}...

Create a comprehensive solution including:
- Solution approach
- Step-by-step implementation plan
- Resource requirements
- Expected outcomes""",
            metadata={"phase": "problem_solving", "problem": problem}
        )
        
        self._record_execution("problem_solver", "solution_design", solution_response)
        print(f"Solution designed: {solution_response['content'][:200]}...\n")
        
        # Step 5: Critical evaluation phase
        print("Step 5: Critical evaluation phase...")
        critique_response = self.critic.think(
            f"""Critically evaluate the proposed solution:

Problem: {problem}

Proposed solution:
{solution_response['content']}

Provide critical evaluation including:
- Strengths of the solution
- Weaknesses and gaps
- Potential risks
- Suggested improvements""",
            metadata={"phase": "critique", "problem": problem}
        )
        
        self._record_execution("critic", "critique", critique_response)
        print(f"Critique completed: {critique_response['content'][:200]}...\n")
        
        # Step 6: Refinement phase
        print("Step 6: Solution refinement phase...")
        refined_solution_response = self.problem_solver.think(
            f"""Refine the solution based on the critique:

Original solution:
{solution_response['content']}

Critique:
{critique_response['content']}

Provide a refined solution that addresses the concerns raised.""",
            metadata={"phase": "refinement", "problem": problem}
        )
        
        self._record_execution("problem_solver", "refinement", refined_solution_response)
        print(f"Solution refined: {refined_solution_response['content'][:200]}...\n")
        
        # Step 7: Final synthesis
        print("Step 7: Final synthesis phase...")
        final_report_response = self.synthesizer.think(
            f"""Synthesize all the work into a comprehensive final report:

Problem: {problem}

Research:
{research_response['content'][:500]}...

Analysis:
{analysis_response['content'][:500]}...

Refined solution:
{refined_solution_response['content']}

Create a comprehensive final report including:
- Executive summary
- Problem analysis
- Solution overview
- Implementation plan
- Key recommendations
- Conclusion""",
            metadata={"phase": "synthesis", "problem": problem}
        )
        
        self._record_execution("synthesizer", "final_report", final_report_response)
        print(f"Final report completed!\n")
        
        print(f"{'='*80}")
        print(f"MULTI-AGENT SYSTEM: Problem-solving process completed")
        print(f"{'='*80}\n")
        
        return {
            "problem": problem,
            "final_report": final_report_response["content"],
            "execution_history": self.execution_history,
            "total_interactions": len(self.execution_history)
        }
    
    def _record_execution(self, agent_name: str, phase: str, response: Dict[str, Any]):
        """Record an agent's execution in the history."""
        self.execution_history.append({
            "agent": agent_name,
            "phase": phase,
            "request_id": response["request_id"],
            "content_preview": response["content"][:200] if response["content"] else "",
            "has_reasoning": bool(response.get("reasoning"))
        })
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get a summary of the execution."""
        agent_counts = {}
        for record in self.execution_history:
            agent = record["agent"]
            agent_counts[agent] = agent_counts.get(agent, 0) + 1
        
        return {
            "total_interactions": len(self.execution_history),
            "agents_used": agent_counts,
            "phases": [record["phase"] for record in self.execution_history]
        }
    
    def save_results(self, results: Dict[str, Any], filename: str = "results.json"):
        """Save results to a file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Results saved to {filename}")
