from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start, router
from .crews.debater1.debater1_crew import Debater1Crew
from .crews.debater2.debater2_crew import Debater2Crew
from .crews.evaluator.evaluator_crew import EvaluatorCrew
# from .crews.moderator.moderator_crew import ModeratorCrew  # Optional

import json

class DebateState(BaseModel):
    topic: str = ""
    debater1_name: str = "Debater 1"
    debater2_name: str = "Debater 2"
    iteration: int = 0
    max_iterations: int = 5
    conversation_history: list = []
    previous_statement: str = ""
    next_debater: str = ""

class DebateFlow(Flow[DebateState]):

    @start()
    def kickoff_debate(self):
        # Initialize the debate
        print(f"Debate started on topic: {self.state.topic}")
        self.state.iteration = 0
        self.state.next_debater = self.state.debater1_name
        self.state.previous_statement = ""
        return "next_turn"

    @router(kickoff_debate)
    def next_turn(self):
        if self.state.iteration >= self.state.max_iterations:
            return "end_debate"
        else:
            if self.state.next_debater == self.state.debater1_name:
                return "debater1_turn"
            else:
                return "debater2_turn"

    @listen("debater1_turn")
    def debater1_turn(self):
        print(f"{self.state.debater1_name}'s turn.")
        # Load style traits
        debater_name = self.state.debater1_name
        filename = f'data/{debater_name.lower().replace(" ", "_")}_style.json'
        with open(filename, 'r') as file:
            style_data = json.load(file)
        style_traits = style_data['style_traits']
        # Pass 'style_traits' into the inputs
        debater = Debater1Crew()
        result = debater.crew().kickoff(inputs={
            "debater_name": debater_name,
            "style_traits": style_traits,
            "topic": self.state.topic,
            "previous_statement": self.state.previous_statement
        })
        response = result.raw.strip()
        # Evaluator
        evaluator = EvaluatorCrew()
        eval_result = evaluator.crew().kickoff(inputs={
            "debater_name": debater_name,
            "response": response
        })
        # Parse the evaluator's response
        try:
            eval_result_json = json.loads(eval_result.raw)
            is_valid = eval_result_json["is_valid"]
            feedback = eval_result_json.get("feedback", "")
        except json.JSONDecodeError as e:
            print(f"Failed to parse evaluator's response: {e}")
            is_valid = False
            feedback = "Invalid response format from evaluator."
        # Proceed with the rest of your logic
        if is_valid:
            self.state.conversation_history.append({
                "debater": debater_name,
                "statement": response
            })
            self.save_conversation()
            self.state.previous_statement = response
            self.state.next_debater = self.state.debater2_name
        else:
            print(f"Evaluator rejected {debater_name}'s response. Feedback: {feedback}")
            return "end_debate"
        self.state.iteration += 1
        return "next_turn"

    @listen("debater2_turn")
    def debater2_turn(self):
        print(f"{self.state.debater2_name}'s turn.")
        # Load style traits
        debater_name = self.state.debater2_name
        filename = f'data/{debater_name.lower().replace(" ", "_")}_style.json'
        with open(filename, 'r') as file:
            style_data = json.load(file)
        style_traits = style_data['style_traits']
        # Pass 'style_traits' into the inputs
        debater = Debater2Crew()
        result = debater.crew().kickoff(inputs={
            "debater_name": debater_name,
            "style_traits": style_traits,
            "topic": self.state.topic,
            "previous_statement": self.state.previous_statement
        })
        response = result.raw.strip()
        # Evaluator
        evaluator = EvaluatorCrew()
        eval_result = evaluator.crew().kickoff(inputs={
            "debater_name": debater_name,
            "response": response
        })
        # Parse the evaluator's response
        try:
            eval_result_json = json.loads(eval_result.raw)
            is_valid = eval_result_json["is_valid"]
            feedback = eval_result_json.get("feedback", "")
        except json.JSONDecodeError as e:
            print(f"Failed to parse evaluator's response: {e}")
            is_valid = False
            feedback = "Invalid response format from evaluator."
        # Proceed with the rest of your logic
        if is_valid:
            self.state.conversation_history.append({
                "debater": debater_name,
                "statement": response
            })
            self.save_conversation()
            self.state.previous_statement = response
            self.state.next_debater = self.state.debater1_name
        else:
            print(f"Evaluator rejected {debater_name}'s response. Feedback: {feedback}")
            return "end_debate"
        self.state.iteration += 1
        return "next_turn"

    @listen("end_debate")
    def end_debate(self):
        print("Debate ended.")
        self.save_conversation(final=True)

    def save_conversation(self, final=False):
        iteration = self.state.iteration
        filename = f"outputs/debate_round_{iteration}.txt" if not final else "outputs/debate_final.txt"
        with open(filename, "w") as f:
            for entry in self.state.conversation_history:
                f.write(f"{entry['debater']}: {entry['statement']}\n")

def kickoff():
    topic = input("Enter the debate topic: ")
    debater1_name = input("Enter Debater 1's name: ")
    debater2_name = input("Enter Debater 2's name: ")

    debate_flow = DebateFlow()
    debate_flow.state.topic = topic
    debate_flow.state.debater1_name = debater1_name
    debate_flow.state.debater2_name = debater2_name
    debate_flow.kickoff()

def plot():
    debate_flow = DebateFlow()
    debate_flow.plot("debate_flow_plot")

if __name__ == "__main__":
    kickoff()
