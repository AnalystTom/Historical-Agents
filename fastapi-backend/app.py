from fastapi import FastAPI

from debate_agent import debate_agent

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "Debate App"}
