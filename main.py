"""
Main Entry Point for Multi-Agent System
Demonstrates solving complex problems with multiple agents.
"""

import json
import sys
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
    """Run the multi-agent system on complex problems."""
    
    print_section("MULTI-AGENT SYSTEM DEMONSTRATION")
    
    # Initialize the system
    print("Initializing Multi-Agent System...")
    logger = LLMLogger(log_dir="llm_logs")
    llm_client = LLMClient(logger=logger)
    mas = MultiAgentSystem(llm_client)
    print(f"✓ System initialized with 6 specialized agents")
    print(f"✓ Logging directory: {logger.log_dir}")
    
    # Define complex problems to solve
    problems = [
        {
            "title": "Climate Change Adaptation Strategy",
            "description": """Design a comprehensive climate change adaptation strategy for a coastal city 
with 500,000 inhabitants that is facing rising sea levels, increased storm intensity, 
and extreme heat events. The strategy should address infrastructure, economic sustainability, 
social equity, and ecological preservation. Consider a 30-year timeline and limited budget."""
        },
        {
            "title": "AI Ethics Framework",
            "description": """Develop a comprehensive AI ethics framework for a large technology company 
that develops consumer AI products. The framework should address bias, privacy, transparency, 
accountability, safety, and societal impact. It should include governance structures, 
evaluation metrics, and implementation guidelines."""
        },
        {
            "title": "Global Supply Chain Optimization",
            "description": """Design an optimization strategy for a global manufacturing company's supply chain 
that currently spans 30 countries. The strategy must reduce costs by 20%, improve delivery times by 30%, 
reduce carbon emissions by 40%, while maintaining quality and resilience against disruptions. 
Consider geopolitical risks, technological solutions, and sustainability requirements."""
        }
    ]
    
    # Solve each problem
    all_results = []
    
    for i, problem in enumerate(problems, 1):
        print_section(f"PROBLEM {i}: {problem['title']}")
        print(f"Description: {problem['description']}\n")
        
        try:
            # Solve the problem using the multi-agent system
            results = mas.solve(problem['description'])
            
            # Print results
            print_section(f"FINAL REPORT FOR PROBLEM {i}")
            print(results['final_report'])
            print("\n")
            
            # Print execution summary
            summary = mas.get_execution_summary()
            print_section("EXECUTION SUMMARY")
            print(f"Total agent interactions: {summary['total_interactions']}")
            print(f"Agents used: {json.dumps(summary['agents_used'], indent=2)}")
            print(f"Phases executed: {', '.join(summary['phases'])}")
            
            # Save individual problem results
            output_file = f"problem_{i}_results.json"
            mas.save_results(results, output_file)
            
            all_results.append({
                "problem_number": i,
                "title": problem['title'],
                "results": results
            })
            
        except Exception as e:
            print(f"Error solving problem {i}: {e}")
            import traceback
            traceback.print_exc()
    
    # Save all results
    print_section("SAVING ALL RESULTS")
    with open("all_results.json", 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print("✓ All results saved to all_results.json")
    
    # Print final statistics
    print_section("FINAL STATISTICS")
    logger_summary = logger.get_session_summary()
    print(f"Session ID: {logger_summary['session_id']}")
    print(f"Total LLM requests: {logger_summary['total_requests']}")
    print(f"Log directory: {logger_summary['log_directory']}")
    print(f"Problems solved: {len(all_results)}")
    
    # List all log files
    log_files = list(Path(logger.log_dir).glob("*.json")) + list(Path(logger.log_dir).glob("*.jsonl"))
    print(f"\nLog files created: {len(log_files)}")
    for log_file in sorted(log_files)[:10]:  # Show first 10
        print(f"  - {log_file.name}")
    if len(log_files) > 10:
        print(f"  ... and {len(log_files) - 10} more")
    
    print_section("DEMONSTRATION COMPLETE")
    print("All LLM interactions have been logged and committed.")
    print(f"Check the '{logger.log_dir}' directory for detailed logs.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
