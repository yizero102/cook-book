from multi_agent_system.agents.base_agent import BaseAgent

class WorkerAgent(BaseAgent):
    def __init__(self, name):
        super().__init__(name, "Worker Agent")

    def execute_task(self, task: str):
        print(f"Worker {self.name} is executing task: {task}")
        messages = [
            {"role": "system", "content": f"You are a world-class researcher. Your name is {self.name}."},
            {"role": "user", "content": f"Research the following topic: {task}. Provide a concise summary of your findings."},
        ]
        response = self._invoke_llm(messages)
        return response.choices[0].message.content
