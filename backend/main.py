# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
import os
from datetime import datetime
import json
import random

def load_api_key():
    try:
        load_dotenv()
        api_key = os.getenv("API_KEY")
        if not api_key:
            raise ValueError("API key not found. Please add your API_KEY to the .env file.")
        return api_key
    except Exception as e:
        raise RuntimeError(f"Error loading API key: {e}")

api_key = load_api_key()
openai.api_key = api_key


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],  # Update this to match your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set your OpenAI API key

class GameState(BaseModel):
    session_id: str
    current_figure: str
    questions_asked: int
    current_score: int

class QuestionRequest(BaseModel):
    session_id: str
    question: str

class GuessRequest(BaseModel):
    session_id: str
    guess: str

class AIResponse(BaseModel):
    content: str
    tokens_used: int

# In-memory store for simplicity; replace with a database in production
game_sessions = {}

# Load historical figures from JSON file
def load_historical_figures(file_path='historical_figures.json'):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data['historicalFigures']

# Select a random historical figure and return only the name
def select_random_figure(figures):
    return random.choice(figures)['name']

@app.post("/api/start-guessing-game", response_model=GameState)
async def start_guessing_game():
    session_id = str(len(game_sessions) + 1)  # Simple session ID generation
    current_figure_name = select_random_figure(load_historical_figures())
    game_sessions[session_id] = {
        "current_figure": current_figure_name,
        "questions_asked": 0,
        "current_score": 1000
    }
    return GameState(session_id=session_id, current_figure=current_figure_name, questions_asked=0, current_score=1000)
    

# Ask a question
@app.post("/api/ask-question", response_model=AIResponse)
async def ask_question(request: QuestionRequest):
    session = game_sessions.get(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session['questions_asked'] >= 10:
        raise HTTPException(status_code=400, detail="Maximum questions reached")

    # Construct context for the question
    context = f"You are {session['current_figure']}. {request.question}"

    response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a historical figure answering questions about yourself within the context of the game."},
                {"role": "user", "content": context}
            ],
            max_tokens=500,
            temperature=0.7
        )

    session['questions_asked'] += 1
    session['current_score'] = max(0, session['current_score'] - 100)

    return AIResponse(
        content=response.choices[0].text.strip(),
        tokens_used=response.usage.total_tokens
    )
    
# Make a guess@app.post("/api/make-guess", response_model=AIResponse)
async def make_guess(request: GuessRequest):
    session = game_sessions.get(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if request.guess.lower() == session['current_figure'].lower():
        session['current_score'] += 500  # Bonus for correct guess
        return AIResponse(content="Correct! You've guessed the figure.", tokens_used=0)
    else:
        session['current_score'] = max(0, session['current_score'] - 50)
        return AIResponse(content="Incorrect guess. Try again!", tokens_used=0)

# To run the server, use: uvicorn main:app --reload