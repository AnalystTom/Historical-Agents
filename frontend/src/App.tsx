import React, { useState } from 'react';
import { BookOpen, Users, Trophy, ArrowLeft } from 'lucide-react';
import GameMenu from './components/GameMenu';
import GuessingGame from './components/GuessingGame';
import DebateSimulator from './components/DebateSimulator';
import { GameMode } from './types';

function App() {
  const [gameMode, setGameMode] = useState<GameMode | null>(null);
  const [totalScore, setTotalScore] = useState(0);

  const handleScoreUpdate = (points: number) => {
    setTotalScore(prev => prev + points);
  };

  const returnToMenu = () => {
    setGameMode(null);
  };

  return (
    <div className="min-h-screen bg-[url('https://images.unsplash.com/photo-1509024644558-2f56ce76c490?q=80&w=2000&auto=format')] bg-cover bg-center bg-no-repeat before:content-[''] before:absolute before:inset-0 before:bg-black/60 before:z-0 relative text-white">
      <div className="container mx-auto px-4 py-8 relative z-10">
        <header className="flex justify-between items-center mb-8">
          <div className="flex items-center gap-4">
            {gameMode && (
              <button
                onClick={returnToMenu}
                className="p-2 hover:bg-white/10 rounded-full transition-colors"
              >
                <ArrowLeft size={24} />
              </button>
            )}
            <h1 className="text-3xl font-bold">Hist Agents</h1>
          </div>
          <div className="flex items-center gap-2 bg-white/10 backdrop-blur-sm px-4 py-2 rounded-full">
            <Trophy size={20} />
            <span className="font-semibold">{totalScore}</span>
          </div>
        </header>

        <main className="max-w-4xl mx-auto">
          {!gameMode && <GameMenu onSelectMode={setGameMode} />}
          
          {gameMode === 'guessing' && (
            <GuessingGame onScoreUpdate={handleScoreUpdate} />
          )}
          
          {gameMode === 'debate' && (
            <DebateSimulator onScoreUpdate={handleScoreUpdate} />
          )}
        </main>
      </div>
    </div>
  );
}

export default App;