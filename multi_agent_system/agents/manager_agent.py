from multi_agent_system.agents.base_agent import BaseAgent
from multi_agent_system.agents.worker_agent import WorkerAgent

class ManagerAgent(BaseAgent):
    def __init__(self, name, workers: list[WorkerAgent]):
        super().__init__(name, "Manager Agent")
        self.workers = workers

    def execute_task(self, task: str):
        print(f"Manager {self.name} is executing task: {task}")

        # 1. Deconstruct the task
        sub_tasks = self._deconstruct_task(task)
        print(f"Deconstructed into sub-tasks: {sub_tasks}")

        # 2. Delegate sub-tasks to workers
        worker_results = []
        for i, sub_task in enumerate(sub_tasks):
            worker = self.workers[i % len(self.workers)]
            result = worker.execute_task(sub_task)
            worker_results.append(result)

        # 3. Aggregate results and generate a final report
        final_report = self._aggregate_results(task, worker_results)
        print(f"Final Report:\n{final_report}")
        return final_report

    def _deconstruct_task(self, task: str) -> list[str]:
        messages = [
            {"role": "system", "content": "You are a project manager. Your job is to break down a complex task into a series of smaller, manageable sub-tasks for your team of researchers."},
            {"role": "user", "content": f"Deconstruct the following research task into 3 sub-tasks: {task}. Return the sub-tasks as a JSON list of strings."},
        ]
        response = self._invoke_llm(messages)
        sub_tasks_str = response.choices[0].message.content
        
        import json
        try:
            return json.loads(sub_tasks_str)
        except json.JSONDecodeError:
            # Try to extract json from markdown
            if sub_tasks_str.startswith("```json"):
                sub_tasks_str = sub_tasks_str[7:-4]
            return json.loads(sub_tasks_str)

    def _aggregate_results(self, original_task: str, worker_results: list[str]) -> str:
        messages = [
            {"role": "system", "content": "You are a senior researcher. Your job is to synthesize a final report from the research findings of your team."},
            {"role": "user", "content": f"The original research task was: {original_task}. Your team has produced the following findings:\n\n{''.join(worker_results)}\n\nPlease synthesize these findings into a single, coherent report."},
        ]
        response = self._invoke_llm(messages)
        return response.choices[0].message.content
