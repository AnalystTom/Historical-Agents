from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class Debater1Crew:
    """Debater 1 Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def debater_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['debater_agent'],
        )

    @task
    def generate_response(self) -> Task:
        return Task(
            config=self.tasks_config['generate_response'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Debater 1 Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            memory=True,
            verbose=True,
        )
