import React, { useState, useEffect } from 'react';
import { historicalFigures } from '../data/historicalFigures';
import { GameState, HistoricalFigure } from '../types';
import axios from 'axios';

interface GuessingGameProps {
  onScoreUpdate: (points: number) => void;
}

function GuessingGame({ onScoreUpdate }: GuessingGameProps) {
  const [currentFigure, setCurrentFigure] = useState<HistoricalFigure | null>(null);
  const [gameState, setGameState] = useState<GameState>({
    questionsAsked: 0,
    currentScore: 1000,
    isGameOver: false,
  });
  const [userGuess, setUserGuess] = useState('');
  const [userQuestion, setUserQuestion] = useState('');
  const [feedback, setFeedback] = useState('');
  const [revealedHints, setRevealedHints] = useState<string[]>([]);
  const [apiResponse, setApiResponse] = useState('');

  useEffect(() => {
    const randomFigure = historicalFigures[Math.floor(Math.random() * historicalFigures.length)];
    setCurrentFigure(randomFigure);
  }, []);

  const handleAskQuestion = async () => {
    if (gameState.questionsAsked >= 10 || !currentFigure || !userQuestion) return;

    try {
      const response = await axios.post('/api/guess', {
        question: userQuestion,
        correct_answer: currentFigure.name
      });

      const hint = response.data.content;

      setGameState(prev => ({
        ...prev,
        questionsAsked: prev.questionsAsked + 1,
        currentScore: Math.max(0, prev.currentScore - 100),
      }));

      setApiResponse(hint);
      setRevealedHints(prev => [...prev, hint]);
    } catch (error) {
      console.error('Error fetching hint:', error);
    }
  };

  const handleGuess = async () => {
    if (!currentFigure) return;

    try {
      const response = await axios.post('/api/guess', {
        question: userGuess,
        correct_answer: currentFigure.name
      });

      const feedbackMessage = response.data.content;

      if (userGuess.toLowerCase() === currentFigure.name.toLowerCase()) {
        setFeedback('Correct! Well done!');
        setGameState(prev => ({ ...prev, isGameOver: true }));
        onScoreUpdate(gameState.currentScore);
      } else {
        setFeedback(feedbackMessage || 'Incorrect. Try again!');
        setGameState(prev => ({
          ...prev,
          currentScore: Math.max(0, prev.currentScore - 50),
        }));
      }
    } catch (error) {
      console.error('Error checking guess:', error);
    }
  };

  if (!currentFigure) return <div>Loading...</div>;

  return (
    <div className="space-y-8">
      <div className="bg-white/10 rounded-xl p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold">Questions Remaining: {10 - gameState.questionsAsked}</h2>
          <div className="text-xl">Score: {gameState.currentScore}</div>
        </div>

        <div className="space-y-4">
          <div className="bg-white/5 rounded-lg p-4">
            <h3 className="font-semibold mb-2">Revealed Hints:</h3>
            {revealedHints.map((hint, index) => (
              <p key={index} className="text-gray-300">{hint}</p>
            ))}
          </div>

          <div className="flex gap-4 mt-4">
            <input
              type="text"
              value={userGuess}
              onChange={(e) => setUserGuess(e.target.value)}
              placeholder="Enter your guess..."
              className="flex-1 bg-white/5 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
            <button
              onClick={handleGuess}
              className="bg-purple-600 hover:bg-purple-700 px-6 py-2 rounded-lg transition-colors"
            >
              Guess
            </button>
          </div>

          <div className="flex gap-4">
            <input
              type="text"
              value={userQuestion}
              onChange={(e) => setUserQuestion(e.target.value)}
              placeholder="Ask a question..."
              className="flex-1 bg-white/5 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
            />
            <button
              onClick={handleAskQuestion}
              className="bg-purple-600 hover:bg-purple-700 px-6 py-2 rounded-lg transition-colors"
            >
              Ask
            </button>
          </div>

          {apiResponse && (
            <div className="p-4 bg-blue-500/20 rounded-lg mt-2">
              <strong>Response:</strong> {apiResponse}
            </div>
          )}

          {feedback && (
            <div className={`p-4 rounded-lg ${feedback.includes('Correct') ? 'bg-green-500/20' : 'bg-red-500/20'}`}>
              {feedback}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default GuessingGame;