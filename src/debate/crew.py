# src/debate/crew.py

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import JSONSearchTool

@CrewBase
class DebateCrew:
    """Debate crew with two debaters and a moderator."""

    def __init__(self):
        super().__init__()
        # Initialize inputs and debater names
        self.inputs = {}
        self.debater_a = None
        self.debater_b = None
        self.debater_a_tool = JSONSearchTool(file_path="./data/debater_a.json")
        self.debater_b_tool = JSONSearchTool(file_path="./data/debater_b.json")

    @agent
    def moderator(self) -> Agent:
        return Agent(
            config=self.agents_config['moderator'],
            verbose=True
        )

    def create_debater_a(self):
        config = self.agents_config['debater_a'].copy()
        config['role'] = config['role'].format(**self.inputs)
        config['backstory'] = (
            config['backstory'].format(**self.inputs) +
            f" Traits: {self.inputs['debater_a_traits']}"
        )
        return Agent(
            config=config,
            verbose=True
        )

    def create_debater_b(self):
        config = self.agents_config['debater_b'].copy()
        config['role'] = config['role'].format(**self.inputs)
        config['backstory'] = (
            config['backstory'].format(**self.inputs) +
            f" Traits: {self.inputs['debater_b_traits']}"
        )
        return Agent(
            config=config,
            verbose=True
        )

    @task
    def select_topic_task(self) -> Task:
        return Task(
            config=self.tasks_config['select_topic_task'],
            run=self.run_select_topic
        )

    @task
    def debate_round_task(self) -> Task:
        return Task(
            config=self.tasks_config['debate_round_task'],
            iterations=1,  # We'll handle iterations in the code
            run=self.run_debate_rounds
        )

    @task
    def declare_winner_task(self) -> Task:
        return Task(
            config=self.tasks_config['declare_winner_task'],
            run=self.run_declare_winner
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Debate crew."""
        return Crew(
            agents=[self.moderator()],  # Call the method to get the agent instance
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

    def run_select_topic(self, task: Task, inputs: dict):
        # Store inputs for use in agent configurations
        self.inputs = inputs

        # Extract the topic and debater names
        topic = inputs.get('topic', '').strip()
        debater_a_name = inputs.get('debater_a_name', '').strip()
        debater_b_name = inputs.get('debater_b_name', '').strip()

        if not topic or not debater_a_name or not debater_b_name:
            print("Missing topic or debater names. Aborting debate.")
            inputs['abort'] = True
            return inputs

        self.inputs['debater_a_name'] = debater_a_name
        self.inputs['debater_b_name'] = debater_b_name

        print(f"Topic Provided: {topic}")

        # Check debaters' qualifications
        qualification_check_prompt = (
            f"Verify if {debater_a_name} and {debater_b_name} are qualified to debate on "
            f"'{topic}'. Provide a brief confirmation."
        )
        qualification_response = self.moderator().run(
            task_description=qualification_check_prompt
        )

        # If not qualified, abort the debate
        if 'not qualified' in qualification_response.lower():
            print("Debaters are not qualified. Aborting debate.")
            inputs['abort'] = True
            return inputs

        # Fetch traits for debaters
        self.inputs['debater_a_traits'] = self.get_traits(debater_a_name)
        self.inputs['debater_b_traits'] = self.get_traits(debater_b_name)

        # Initialize debaters with updated configurations
        self.debater_a = self.create_debater_a()
        self.debater_b = self.create_debater_b()

        # Pass the topic to the next tasks
        inputs['topic'] = topic
        inputs['qualification'] = qualification_response
        print(f"Qualification Check: {qualification_response}")
        return inputs

    def get_traits(self, name):
        """Fetch traits for a given famous person using the model."""
        prompt = (
            f"Provide a brief description of {name}, highlighting their key traits, "
            "accomplishments, and debating style."
        )
        response = self.moderator().run(task_description=prompt)
        return response.strip()

    def run_debate_rounds(self, task: Task, inputs: dict):
        # Check if the debate was aborted
        if inputs.get('abort', False):
            print("Debate aborted due to unqualified debaters.")
            return inputs

        # Initialize chat history
        chat_history = inputs.get('chat_history', [])
        topic = inputs['topic']
        debater_a_name = self.inputs['debater_a_name']
        debater_b_name = self.inputs['debater_b_name']
        total_rounds = 10  # Number of rounds

        for i in range(total_rounds):
            print(f"\n--- Debate Round {i+1} ---\n")

            # Prepare the conversation history
            conversation_history = ""
            for j in range(i):
                conversation_history += f"Round {j+1}:\n"
                conversation_history += f"{debater_a_name}: {chat_history[j]['debater_a']}\n"
                conversation_history += f"{debater_b_name}: {chat_history[j]['debater_b']}\n\n"

            # Debater A's turn
            debater_a_prompt = (
                f"Debate Topic: {topic}\nRound {i+1}\nAs {debater_a_name}, present your argument.\n"
            )
            if conversation_history:
                debater_a_prompt += f"Previous Rounds:\n{conversation_history}\n"
                debater_a_prompt += f"Your opponent's last argument: {chat_history[i-1]['debater_b']}\n"

            debater_a_response = self.debater_a.run(
                task_description=debater_a_prompt
            )

            # Debater B's turn
            debater_b_prompt = (
                f"Debate Topic: {topic}\nRound {i+1}\nAs {debater_b_name}, present your argument.\n"
            )
            if conversation_history or debater_a_response:
                debater_b_prompt += f"Previous Rounds:\n{conversation_history}\n"
                debater_b_prompt += f"Your opponent's last argument: {debater_a_response}\n"

            debater_b_response = self.debater_b.run(
                task_description=debater_b_prompt
            )

            # Update chat history
            chat_history.append({
                'debater_a': debater_a_response,
                'debater_b': debater_b_response
            })

            # Print arguments
            print(f"{debater_a_name}:\n{debater_a_response}\n")
            print(f"{debater_b_name}:\n{debater_b_response}\n")

        # Pass the chat history to the next task
        inputs['chat_history'] = chat_history
        return inputs

    def run_declare_winner(self, task: Task, inputs: dict):
        # Check if the debate was aborted
        if inputs.get('abort', False):
            print("Debate aborted. No winner declared.")
            return inputs

        # Moderator evaluates the debate
        debater_a_name = self.inputs['debater_a_name']
        debater_b_name = self.inputs['debater_b_name']
        evaluation_prompt = (
            f"Based on the following debate between {debater_a_name} and {debater_b_name}, "
            "declare the winner and provide justification:\n\n"
        )
        for i, round_data in enumerate(inputs['chat_history']):
            evaluation_prompt += f"**Round {i+1}:**\n"
            evaluation_prompt += f"{debater_a_name}: {round_data['debater_a']}\n"
            evaluation_prompt += f"{debater_b_name}: {round_data['debater_b']}\n\n"

        winner_announcement = self.moderator().run(
            task_description=evaluation_prompt
        )

        print("Winner Announcement:\n")
        print(winner_announcement)
        return inputs
