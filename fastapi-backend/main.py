from fastapi import FastAPI
from pydantic import BaseModel
from langgraph.checkpoint.memory import MemorySaver

from debate_agent import debate_agent

class DebateInput(BaseModel):
    topic: str
    pro_debator: str
    anti_debator: str

memory = MemorySaver()

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "Debate App"}

@app.post('/debate')
async def debate(input: DebateInput):
    state = {
        "topic": input.topic,
        "pro_debator": input.pro_debator,
        "anti_debator": input.anti_debator,
        "greetings": "",
        "planning": "",
        "pro_debator_response": "",
        "anti_debator_response": "",
        "context": [],
        "debate": [],
        "debate_history": [],
        "iteration": 0,
        "max_iteration": 3,
        "winner": "",
    }
    response = debate_agent(memory=memory, state=state)
    return response