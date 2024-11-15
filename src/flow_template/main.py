from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start
from .crews.debater1.debater1_crew import Debater1Crew
from .crews.debater2.debater2_crew import Debater2Crew
from .crews.evaluator.evaluator_crew import EvaluatorCrew
import json
import os
import asyncio  # Import asyncio for asynchronous operations
# Import FastAPI and WebSockets
from fastapi import FastAPI, WebSocket
import uvicorn
import logging  # Import logging module

# Import OpenTelemetry modules
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

# Initialize the TracerProvider only once
trace.set_tracer_provider(TracerProvider())

# Set logging level to suppress OpenTelemetry warnings
logging.getLogger('opentelemetry').setLevel(logging.ERROR)


app = FastAPI()

class DebateState(BaseModel):
    topic: str = ""
    debater1_name: str = "Debater 1"
    debater2_name: str = "Debater 2"
    iteration: int = 0
    max_iterations: int = 2
    conversation_history: list = []
    previous_statement: str = ""

class DebateFlow(Flow[DebateState]):

    def __init__(self, websocket: WebSocket):
        super().__init__()
        self.websocket = websocket  # Store websocket as an instance variable
        self.debate_finished = asyncio.Event()  # Event to signal when debate is over

        # Instantiate crew instances once
        self.debater1 = Debater1Crew()
        self.debater2 = Debater2Crew()
        self.evaluator = EvaluatorCrew()

    @start()
    async def kickoff_debate(self):
        # Initialize the debate
        print(f"Debate started on topic: {self.state.topic}")
        self.state.iteration = 0
        self.state.previous_statement = ""
        # Schedule debater1's turn without awaiting
        asyncio.create_task(self.debater1_turn())

    async def debater1_turn(self):
        # Debater 1's turn
        print(f"{self.state.debater1_name}'s turn.")
        debater_name = self.state.debater1_name
        response = await self._get_response(debater_name, self.debater1)

        if response:
            self.state.previous_statement = response
            # Schedule debater2's turn
            asyncio.create_task(self.debater2_turn())
        else:
            # Schedule end of debate
            asyncio.create_task(self.end_debate())

    async def debater2_turn(self):
        # Debater 2's turn
        print(f"{self.state.debater2_name}'s turn.")
        debater_name = self.state.debater2_name
        response = await self._get_response(debater_name, self.debater2)

        if response:
            self.state.previous_statement = response
            # Schedule check_iteration
            asyncio.create_task(self.check_iteration())
        else:
            # Schedule end of debate
            asyncio.create_task(self.end_debate())

    async def check_iteration(self):
        # Check if maximum iterations reached
        self.state.iteration += 1
        print(f"Iteration completed: {self.state.iteration}")
        if self.state.iteration >= self.state.max_iterations:
            # Schedule end of debate
            asyncio.create_task(self.end_debate())
        else:
            # Schedule debater1's turn
            asyncio.create_task(self.debater1_turn())

    async def end_debate(self):
        # End the debate
        print("Debate ended.")
        self.save_conversation(final=True)
        # Notify frontend that debate has ended
        if self.websocket:
            await self.websocket.send_json({"event": "debate_ended"})
        # Signal that the debate is finished
        self.debate_finished.set()

    async def _get_response(self, debater_name, debater_instance):
        """Helper method to handle debater response and evaluation."""
        filename = f'data/{debater_name.lower().replace(" ", "_")}_style.json'
        try:
            with open(filename, 'r') as file:
                style_data = json.load(file)
            style_traits = style_data['style_traits']
        except FileNotFoundError:
            print(f"Style file not found for {debater_name}.")
            style_traits = []

        # Get response from the debater in an executor
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, debater_instance.crew().kickoff, {
            "debater_name": debater_name,
            "style_traits": style_traits,
            "topic": self.state.topic,
            "previous_statement": self.state.previous_statement
        })
        response = result.raw.strip()

        # Evaluate the response in an executor
        eval_result = await loop.run_in_executor(None, self.evaluator.crew().kickoff, {
            "debater_name": debater_name,
            "response": response
        })

        try:
            eval_result_json = json.loads(eval_result.raw)
            is_valid = eval_result_json["is_valid"]
            feedback = eval_result_json.get("feedback", "")
        except json.JSONDecodeError as e:
            print(f"Failed to parse evaluator's response: {e}")
            is_valid = False
            feedback = "Invalid response format from evaluator."

        if is_valid:
            self.state.conversation_history.append({
                "debater": debater_name,
                "statement": response
            })
            self.save_conversation()
            # Send response to frontend immediately
            if self.websocket:
                await self.websocket.send_json({
                    "debater": debater_name,
                    "statement": response
                })
            return response
        else:
            print(f"Evaluator rejected {debater_name}'s response. Feedback: {feedback}")
            # Send rejection to frontend immediately
            if self.websocket:
                await self.websocket.send_json({
                    "debater": debater_name,
                    "error": feedback
                })
            return None

    def save_conversation(self, final=False):
        iteration = self.state.iteration
        os.makedirs("outputs", exist_ok=True)
        filename = f"outputs/debate_round_{iteration}.txt" if not final else "outputs/debate_final.txt"
        with open(filename, "w") as f:
            for entry in self.state.conversation_history:
                f.write(f"{entry['debater']}: {entry['statement']}\n")

# FastAPI endpoint to start the debate
@app.websocket("/debate")
async def debate_endpoint(websocket: WebSocket):
    await websocket.accept()
    # Receive initial data from frontend
    data = await websocket.receive_json()
    topic = data.get("topic")
    debater1_name = data.get("debater1_name")
    debater2_name = data.get("debater2_name")
    max_iterations = data.get("max_iterations", 2)

    debate_flow = DebateFlow(websocket)
    debate_flow.state.topic = topic
    debate_flow.state.debater1_name = debater1_name
    debate_flow.state.debater2_name = debater2_name
    debate_flow.state.max_iterations = max_iterations

    # Run the flow
    await debate_flow.kickoff_async()

    # Wait for the debate to finish before closing the WebSocket
    await debate_flow.debate_finished.wait()

    # Close the WebSocket connection
    await websocket.close()

# Run the server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
