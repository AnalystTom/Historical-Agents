from fastapi import FastAPI, Request
from pydantic import BaseModel
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from debate_agent import debate_agent
from fastapi.middleware.cors import CORSMiddleware
import json
class DebateInput(BaseModel):
    topic: str
    pro_debator: str
    anti_debator: str

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

@app.post('/trigger_workflow')
async def debate(request: Request):
    data = await request.json()
    debate_topic = data.get('debate_topic')
    debater1 = data.get('debater1')
    debater2 = data.get('debater2')
    max_iterations = data.get('max_iterations', 1)
    
    state = {
        "topic": debate_topic,
        "pro_debator": debater1,
        "anti_debator": debater2,
        "greetings": "",
        "planning": "",
        "pro_debator_response": "",
        "anti_debator_response": "",
        "context": [],
        "debate": [],
        "debate_history": [],
        "iteration": 0,
        "max_iteration": max_iterations,
        "winner": "",
    }
    
    thread = {"configurable": {"thread_id": "unique_thread_id"}}
    
    # Get response from debate agent
    response = debate_agent(memory=memory, state=state)
    greetings = ""
    winner = ""  # You might need to determine this based on additional logic
    conversation = []
    print("Response from debate_agent:", response)
        
        
    # Since response is a list, we need to process it differently
    
    for message in response:
        if isinstance(message, SystemMessage) and message.name == 'greeting':
            greetings = message.content
        if isinstance(message, SystemMessage) and message.name == 'winner':
            winner = message.content
        elif isinstance(message, HumanMessage):
            conversation.append({
                'speaker': debater1,
                'content': message.content
            })
        elif isinstance(message, AIMessage):
            conversation.append({
                'speaker': debater2,
                'content': message.content
            })
    
    response_data = {
        'greetings': greetings,
        'conversation': conversation,
        'debate_history': state.get('debate_history', []),
        'winner': winner
    }

    return response_data