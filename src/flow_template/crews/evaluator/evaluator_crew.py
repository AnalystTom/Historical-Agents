from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class EvaluatorCrew:
    """Evaluator Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def evaluator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['evaluator_agent'],
        )

    @task
    def evaluate_response(self) -> Task:
        return Task(
            config=self.tasks_config['evaluate_response'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Evaluator Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
