import os
import sys

from multi_agent_system.agents.worker_agent import WorkerAgent
from multi_agent_system.agents.manager_agent import ManagerAgent

def main():
    # 1. Create worker agents
    worker1 = WorkerAgent("Alice")
    worker2 = WorkerAgent("Bob")

    # 2. Create a manager agent
    manager = ManagerAgent("Charlie", workers=[worker1, worker2])

    # 3. Define a complex task
    task = "Research the impact of AI on the future of work, covering both positive and negative aspects."

    # 4. Execute the task
    manager.execute_task(task)

if __name__ == "__main__":
    # A simple check for environment variables
    required_vars = ['_OPENAI_BASE_URL', '_OPENAI_API_KEY', '_MODEL_NAME']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
        sys.exit(1)
        
    main()
