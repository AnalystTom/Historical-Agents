from fastapi import FastAPI, Request
from pydantic import BaseModel
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from debate_agent import debate_agent
from fastapi.middleware.cors import CORSMiddleware
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
    conversation = []
    
    # Since response is a list, we need to process it differently
    for message in response:
        if isinstance(message, dict):
            # If it's a dictionary, process it as before
            if 'greetings' in message:
                conversation.append({
                    'speaker': "Moderator",
                    'content': message['greetings']
                })
        elif isinstance(message, (HumanMessage, AIMessage)):
            # Process debate messages
            speaker = debater1 if isinstance(message, HumanMessage) else debater2
            conversation.append({
                'speaker': speaker,
                'content': message.content
            })
    
    response_data = {
        'conversation': conversation,
        'debate_history': state.get('debate_history', [])
    }

    return response_data