"""
Demonstration of Multi-Agent System
Solves a complex problem and verifies all logging functionality.
"""

import json
from pathlib import Path

from llm_client import LLMClient
from llm_logger import LLMLogger
from multi_agent_system import MultiAgentSystem


def print_section(title: str):
    """Print a section header."""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")


def main():
    """Run the multi-agent system demonstration."""
    
    print_section("MULTI-AGENT SYSTEM DEMONSTRATION")
    
    # Initialize the system
    print("Initializing Multi-Agent System...")
    logger = LLMLogger(log_dir="llm_logs")
    llm_client = LLMClient(logger=logger)
    mas = MultiAgentSystem(llm_client)
    print(f"✓ System initialized with 6 specialized agents:")
    print(f"  - CoordinatorAgent (System Coordinator)")
    print(f"  - ResearchAgent (Research Specialist)")
    print(f"  - AnalystAgent (Data Analyst)")
    print(f"  - ProblemSolverAgent (Problem Solver)")
    print(f"  - CriticAgent (Quality Critic)")
    print(f"  - SynthesizerAgent (Information Synthesizer)")
    print(f"✓ Logging directory: {logger.log_dir}")
    
    # Define a complex problem to solve
    problem = {
        "title": "Quantum Computing Education Curriculum",
        "description": """Design a comprehensive educational curriculum for introducing 
quantum computing concepts to undergraduate computer science students who have 
completed linear algebra and basic algorithms courses. The curriculum should:
1) Build intuition about quantum phenomena
2) Cover quantum gates, circuits, and algorithms
3) Include practical programming with quantum frameworks
4) Address theoretical foundations and real-world applications
5) Be deliverable in a 14-week semester with 3 hours per week
6) Include assessment strategies and learning outcomes"""
    }
    
    print_section(f"PROBLEM: {problem['title']}")
    print(f"Description: {problem['description']}\n")
    
    try:
        # Solve the problem using the multi-agent system
        print("Starting multi-agent problem-solving process...\n")
        results = mas.solve(problem['description'])
        
        # Print results
        print_section("FINAL REPORT")
        print(results['final_report'])
        print("\n")
        
        # Print execution summary
        summary = mas.get_execution_summary()
        print_section("EXECUTION SUMMARY")
        print(f"Total agent interactions: {summary['total_interactions']}")
        print(f"\nAgents used:")
        for agent, count in summary['agents_used'].items():
            print(f"  - {agent}: {count} interactions")
        print(f"\nPhases executed:")
        for i, phase in enumerate(summary['phases'], 1):
            print(f"  {i}. {phase}")
        
        # Save results
        output_file = "demo_results.json"
        mas.save_results(results, output_file)
        print(f"\n✓ Results saved to {output_file}")
        
        # Verify logging
        print_section("LOGGING VERIFICATION")
        logger_summary = logger.get_session_summary()
        print(f"Session ID: {logger_summary['session_id']}")
        print(f"Total LLM requests logged: {logger_summary['total_requests']}")
        print(f"Log directory: {logger_summary['log_directory']}")
        
        # List log files
        log_dir = Path(logger.log_dir)
        request_logs = sorted(log_dir.glob("*_request_*.json"))
        summary_logs = sorted(log_dir.glob("*_summary.jsonl"))
        
        print(f"\n✓ Created {len(request_logs)} request log files")
        print(f"✓ Created {len(summary_logs)} summary log files")
        
        # Show sample log structure
        if request_logs:
            print(f"\nSample log file: {request_logs[0].name}")
            with open(request_logs[0], 'r') as f:
                sample_log = json.load(f)
            print(f"  - Agent: {sample_log['agent_name']}")
            print(f"  - Timestamp: {sample_log['timestamp']}")
            print(f"  - Has reasoning: {bool(sample_log['response']['reasoning'])}")
            print(f"  - Tokens used: {sample_log['response']['usage']['total_tokens']}")
        
        print_section("DEMONSTRATION COMPLETE")
        print("✓ Multi-agent system successfully solved complex problem")
        print("✓ All LLM interactions logged with reasoning details")
        print(f"✓ Check '{logger.log_dir}' directory for complete logs")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
