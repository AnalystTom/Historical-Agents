from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.memory.long_term.long_term_memory import LongTermMemory
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from crewai.memory.short_term.short_term_memory import ShortTermMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.entity.entity_memory import EntityMemory
import os
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

@CrewBase
class Debater2Crew:
    """Debater 2 Crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
    db_storage_path = os.path.join(os.getcwd(), 'debater2')
    print(db_storage_path)

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
            planning=False,
            memory=False,
        #     embedder=OpenAIEmbeddingFunction(api_key=os.getenv("OPENAI_API_KEY"), model_name="text-embedding-3-small"),
        #     long_term_memory=LongTermMemory(
        #     storage=LTMSQLiteStorage(
        #         # db_path="/my_data_dir/debater2/long_term_memory_storage.db"
        #     )
        # ),
    #     short_term_memory=ShortTermMemory(
    #             storage=RAGStorage(
    #             crew="my_crew",
    #             type="short_term",
    #             #data_dir="//my_data_dir",
    #             #model=embedder["model"],
    #             #dimension=embedder["dimension"],
    #         ),
    #     ),
    #     entity_memory=EntityMemory(
    #             storage=RAGStorage(
    #             crew="my_crew",
    #             type="entities",
    #             #data_dir="//my_data_dir",   
    #             #model=embedder["model"],
    #             #dimension=embedder["dimension"],
    #             ),
    # ),
            verbose=True,
        )
