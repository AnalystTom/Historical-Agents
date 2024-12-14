from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from states.additional_states import WinnerResponse

from debate_agent import debate_agent

class DebateInput(BaseModel):
    topic: str
    pro_debator: str
    anti_debator: str
    max_iterations: int

memory = MemorySaver()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def root():
    return {"message": "Debate App"}

# @app.post('/trigger_workflow')
# async def debate(input: DebateInput):
#     debate_topic = input.topic
#     debater1 = input.pro_debator
#     debater2 = input.anti_debator    
#     max_iterations = input.max_iterations
#     state = {
#         "topic": debate_topic,
#         "pro_debator": debater1,
#         "anti_debator": debater2,
#         "pro_debator_response": None,
#         "anti_debator_response": None,
#         "context": [],
#         "debate": [],
#         "debate_history": [],
#         "planner": "",
#         "winner": None,
#         "iteration": 0,
#         "max_iteration": max_iterations,
#         "winner": "",
#     }
    
#     thread = {"configurable": {"thread_id": "unique_thread_id"}}
    
#     # Get response from debate agent
#     response = debate_agent(memory=memory, state=state)
#     print(response)
#     #print(response['winner'].winner)
#     greetings = ""
#     winner = response.get('winner')
#     #winner = ''
#     conversation = []
#     print("Response from debate_agent:", response)
        
        
#     for message in response.get('debate', []):
#         if hasattr(message, 'name') and message.name == 'greeting':
#             greetings = message.content
#         elif hasattr(message, 'name') and message.name == 'winner':
#             winner = message.content
#         elif hasattr(message, 'content'):
#             speaker = debater1 if isinstance(message, HumanMessage) else debater2
#             conversation.append({
#                 'speaker': speaker,
#                 'content': message.content
#             })

#     response_data = {
#         'greetings': greetings,
#         'conversation': conversation,
#         'debate_history': state.get('debate_history', []),
#         'winner': winner
#     }

#     return response_data

from typing import Optional, List, Dict
from fastapi import WebSocket
import asyncio

class WebSocketManager:
    def __init__(self):
        self.websocket: Optional[WebSocket] = None
        self.connection_open = False
        self.last_sent_message = None  # Track the last sent message
        self.speaker = None

    async def set_websocket(self, websocket: WebSocket):
        self.websocket = websocket
        self.connection_open = True

    async def send_update(self, msg_type: str, message: str):
        if self.websocket and self.connection_open:
            # Check if the message is identical to the last sent message
            current_message = {"type": msg_type, "message": message}
            if current_message == self.last_sent_message:
                print("Duplicate message detected. Skipping WebSocket update.")
                return

            self.last_sent_message = current_message  # Update the last sent message
            try:
                await self.websocket.send_json({
                    "type": "new_message",
                    "data": current_message
                })
            except Exception as e:
                print(f"WebSocketManager: Failed to send update. Error: {e}")
        else:
            print("WebSocketManager: Connection not open. Unable to send update.")

    async def close_connection(self):
        """Close the WebSocket connection if it is open."""
        if self.websocket and self.connection_open:
            try:
                print("WebSocketManager: Closing WebSocket connection.")
                await self.websocket.close()
                self.connection_open = False
            except Exception as e:
                print(f"WebSocketManager: Failed to close connection. Error: {e}")
        else:
            print("WebSocketManager: No active connection to close.")


@app.websocket("/ws/debate")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_manager = WebSocketManager()
    await websocket_manager.set_websocket(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            input_data = DebateInput(**data)

            state = {
                "topic": input_data.topic,
                "pro_debator": input_data.pro_debator,
                "anti_debator": input_data.anti_debator,
                "pro_debator_response": None,
                "anti_debator_response": None,
                "context": [],
                "debate": [],
                "debate_history": [],
                "planner": "",
                "winner": None,
                "iteration": 0,
                "max_iteration": input_data.max_iterations,
            }

            # Run debate agent and stream updates
            result = await debate_agent(memory, state, websocket_manager)

            # Ensure the result is JSON serializable
            summary = result.get("summary")
            winner = result.get("winner")

            # Serialize WinnerResponse object using .dict()
            if isinstance(winner, WinnerResponse):
                winner = winner.dict()  # Convert to JSON-serializable dictionary

            # Serialize other objects if needed
            if hasattr(summary, "dict"):
                summary = summary.dict()  # Convert to JSON-serializable dictionary

            # Send final results to the frontend
            await websocket.send_json({
                "type": "final_result",
                "summary": summary,
                "winner": winner,
            })

            # Close the WebSocket connection after sending the final output
            await websocket_manager.close_connection()
            break
    except WebSocketDisconnect:
        print("WebSocket connection closed")
    except Exception as e:
        print(f"Unexpected WebSocket error: {e}")
    finally:
        # Ensure WebSocket is closed gracefully if not already closed
        await websocket_manager.close_connection()
