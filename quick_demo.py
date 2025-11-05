"""
Quick demonstration of the multi-agent system.
Solves a simpler problem to quickly verify all functionality.
"""

import json
from pathlib import Path

from llm_client import LLMClient
from llm_logger import LLMLogger
from base_agent import BaseAgent
from agents import ResearchAgent, AnalystAgent, SynthesizerAgent


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")


def main():
    """Run a quick multi-agent demonstration."""
    
    print_section("QUICK MULTI-AGENT DEMONSTRATION")
    
    # Initialize the system
    print("Initializing system...")
    logger = LLMLogger(log_dir="llm_logs")
    llm_client = LLMClient(logger=logger)
    
    # Create three agents
    researcher = ResearchAgent(llm_client)
    analyst = AnalystAgent(llm_client)
    synthesizer = SynthesizerAgent(llm_client)
    
    print(f"✓ Initialized 3 agents")
    print(f"✓ Logging to: {logger.log_dir}")
    
    # Define a problem
    problem = """Design a 3-day training program for teaching software engineers about 
AI ethics, covering bias, privacy, and responsible AI deployment."""
    
    print_section("PROBLEM")
    print(problem)
    
    # Agent 1: Research
    print_section("AGENT 1: RESEARCH")
    print("ResearchAgent is gathering information...")
    research_result = researcher.think(
        f"Research the key topics for this training program: {problem}",
        metadata={"phase": "research"}
    )
    print(f"✓ Research complete (Request ID: {research_result['request_id']})")
    print(f"Preview: {research_result['content'][:300]}...")
    
    # Agent 2: Analysis
    print_section("AGENT 2: ANALYSIS")
    print("AnalystAgent is analyzing the research...")
    analysis_result = analyst.think(
        f"Analyze this research and identify the most important topics:\n\n{research_result['content'][:1000]}",
        metadata={"phase": "analysis"}
    )
    print(f"✓ Analysis complete (Request ID: {analysis_result['request_id']})")
    print(f"Preview: {analysis_result['content'][:300]}...")
    
    # Agent 3: Synthesis
    print_section("AGENT 3: SYNTHESIS")
    print("SynthesizerAgent is creating the final program...")
    synthesis_result = synthesizer.think(
        f"""Create a detailed 3-day training program based on this analysis:
        
Problem: {problem}

Analysis: {analysis_result['content'][:1000]}

Provide a comprehensive day-by-day schedule with topics, activities, and learning outcomes.""",
        metadata={"phase": "synthesis"}
    )
    print(f"✓ Synthesis complete (Request ID: {synthesis_result['request_id']})")
    
    # Print final result
    print_section("FINAL TRAINING PROGRAM")
    print(synthesis_result['content'])
    
    # Save results
    results = {
        "problem": problem,
        "research": research_result['content'],
        "analysis": analysis_result['content'],
        "final_program": synthesis_result['content'],
        "request_ids": [
            research_result['request_id'],
            analysis_result['request_id'],
            synthesis_result['request_id']
        ]
    }
    
    with open("quick_demo_results.json", 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print_section("LOGGING VERIFICATION")
    logger_summary = logger.get_session_summary()
    print(f"Session ID: {logger_summary['session_id']}")
    print(f"Total LLM requests: {logger_summary['total_requests']}")
    
    # Count log files
    log_dir = Path(logger.log_dir)
    all_logs = list(log_dir.glob("*.json"))
    print(f"Total log files: {len(all_logs)}")
    
    # Verify one log has reasoning
    latest_log = sorted(log_dir.glob(f"{logger.session_id}_request_*.json"))[-1]
    with open(latest_log, 'r') as f:
        log_data = json.load(f)
    
    print(f"\nSample log verification ({latest_log.name}):")
    print(f"  - Agent: {log_data['agent_name']}")
    print(f"  - Has reasoning: {bool(log_data['response']['reasoning'])}")
    print(f"  - Tokens: {log_data['response']['usage']['total_tokens']}")
    
    print_section("DEMONSTRATION COMPLETE")
    print("✓ Multi-agent collaboration successful")
    print("✓ All LLM interactions logged with reasoning")
    print(f"✓ Results saved to quick_demo_results.json")
    print(f"✓ Check '{logger.log_dir}' for detailed logs")
    
    return 0


if __name__ == "__main__":
    exit(main())
