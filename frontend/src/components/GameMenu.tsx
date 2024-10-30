import React from 'react';
import { BookOpen, Users } from 'lucide-react';
import { GameMode } from '../types';

interface GameMenuProps {
  onSelectMode: (mode: GameMode) => void;
}

function GameMenu({ onSelectMode }: GameMenuProps) {
  return (
    <div className="grid md:grid-cols-2 gap-8">
      <button
        onClick={() => onSelectMode('guessing')}
        className="group relative bg-white/10 rounded-2xl p-8 hover:bg-white/20 transition-all duration-300"
      >
        <div className="flex flex-col items-center gap-4">
          <Users size={48} className="text-purple-300" />
          <h2 className="text-2xl font-bold">Historical Figure Guessing</h2>
          <p className="text-center text-gray-300">
            Test your knowledge by identifying historical figures through yes/no questions.
            Limited to 10 questions per round.
          </p>
        </div>
        <div className="absolute bottom-4 right-4 bg-purple-500 px-3 py-1 rounded-full text-sm">
          Play Now
        </div>
      </button>

      <button
        onClick={() => onSelectMode('debate')}
        className="group relative bg-white/10 rounded-2xl p-8 hover:bg-white/20 transition-all duration-300"
      >
        <div className="flex flex-col items-center gap-4">
          <BookOpen size={48} className="text-blue-300" />
          <h2 className="text-2xl font-bold">Historical Debate Simulator</h2>
          <p className="text-center text-gray-300">
            Engage in debates with historical figures on various topics.
            Learn different perspectives from throughout history.
          </p>
        </div>
        <div className="absolute bottom-4 right-4 bg-blue-500 px-3 py-1 rounded-full text-sm">
          Play Now
        </div>
      </button>
    </div>
  );
}

export default GameMenu;