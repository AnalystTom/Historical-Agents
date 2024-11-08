from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class Debater2Crew:
    """Debater 2 Crew"""

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
        """Creates the Debater 2 Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
