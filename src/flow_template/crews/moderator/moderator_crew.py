from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class ModeratorCrew:
    """Moderator Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def moderator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['moderator_agent'],
        )

    @task
    def moderate_discussion(self) -> Task:
        return Task(
            config=self.tasks_config['moderate_discussion'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Moderator Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )