# main.py

from fastapi import FastAPI
from backend.routers import debate, guess

app = FastAPI()

# Include routers
app.include_router(debate.router, prefix="/debate", tags=["Debate"])
app.include_router(guess.router, prefix="/guess", tags=["Guess"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Hist Agents API"}



# To run the server, use: uvicorn main:app --reload