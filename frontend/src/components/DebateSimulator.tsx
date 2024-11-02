import React, { useState } from 'react';
import { debateTopics } from '../data/debateTopics';
import { historicalFigures } from '../data/historicalFigures';
import { DebateTopic, HistoricalFigure } from '../types';
import { UserCircle2, Users } from 'lucide-react';

interface DebateSimulatorProps {
  onScoreUpdate: (points: number) => void;
}

type DebateMode = 'user' | 'ai' | null;

function DebateSimulator({ onScoreUpdate }: DebateSimulatorProps) {
  const [debateMode, setDebateMode] = useState<DebateMode>(null);
  const [selectedFigure, setSelectedFigure] = useState<HistoricalFigure | null>(null);
  const [selectedOpponent, setSelectedOpponent] = useState<HistoricalFigure | null>(null);
  const [selectedTopic, setSelectedTopic] = useState<DebateTopic | null>(null);
  const [debate, setDebate] = useState<Array<{ speaker: string; text: string }>>([]);
  const [userArgument, setUserArgument] = useState('');

  const handleFigureSelect = (figure: HistoricalFigure) => {
    if (!selectedFigure) {
      setSelectedFigure(figure);
    } else if (debateMode === 'ai' && !selectedOpponent) {
      setSelectedOpponent(figure);
    }
    setDebate([]);
  };

  const handleTopicSelect = (topic: DebateTopic) => {
    setSelectedTopic(topic);
    if (debateMode === 'ai') {
      simulateDebate(topic);
    } else {
      setDebate([]);
    }
  };

  const simulateDebate = (topic: DebateTopic) => {
    if (!selectedFigure || !selectedOpponent) return;

    const debate = [];
    const rounds = 3;
    
    for (let i = 0; i < rounds; i++) {
      const firstPerspective = topic.perspectives[selectedFigure.id][i % topic.perspectives[selectedFigure.id].length];
      const secondPerspective = topic.perspectives[selectedOpponent.id][i % topic.perspectives[selectedOpponent.id].length];
      
      debate.push(
        { speaker: selectedFigure.name, text: firstPerspective },
        { speaker: selectedOpponent.name, text: secondPerspective }
      );
    }
    
    setDebate(debate);
    onScoreUpdate(30); // Award points for watching a full debate
  };

  const handleSubmitArgument = () => {
    if (!selectedFigure || !selectedTopic || !userArgument.trim()) return;

    const newDebate = [
      ...debate,
      { speaker: 'You', text: userArgument },
      {
        speaker: selectedFigure.name,
        text: selectedTopic.perspectives[selectedFigure.id][
          Math.floor(Math.random() * selectedTopic.perspectives[selectedFigure.id].length)
        ],
      },
    ];

    setDebate(newDebate);
    setUserArgument('');
    onScoreUpdate(10);
  };

  if (!debateMode) {
    return (
      <div className="grid md:grid-cols-2 gap-8">
        <button
          onClick={() => setDebateMode('user')}
          className="group relative bg-white/10 backdrop-blur-sm rounded-2xl p-8 hover:bg-white/20 transition-all duration-300"
        >
          <div className="flex flex-col items-center gap-4">
            <UserCircle2 size={48} className="text-purple-300" />
            <h2 className="text-2xl font-bold">Debate a Historical Figure</h2>
            <p className="text-center text-gray-300">
              Challenge a historical figure to a debate and test your rhetorical skills.
            </p>
          </div>
          <div className="absolute bottom-4 right-4 bg-purple-500 px-3 py-1 rounded-full text-sm">
            Start Debate
          </div>
        </button>

        <button
          onClick={() => setDebateMode('ai')}
          className="group relative bg-white/10 backdrop-blur-sm rounded-2xl p-8 hover:bg-white/20 transition-all duration-300"
        >
          <div className="flex flex-col items-center gap-4">
            <Users size={48} className="text-blue-300" />
            <h2 className="text-2xl font-bold">Watch Historical Debate</h2>
            <p className="text-center text-gray-300">
              Observe a debate between two historical figures and learn from their perspectives.
            </p>
          </div>
          <div className="absolute bottom-4 right-4 bg-blue-500 px-3 py-1 rounded-full text-sm">
            Watch Debate
          </div>
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {!selectedFigure && (
        <div className="space-y-4">
          <h2 className="text-2xl font-bold">
            {debateMode === 'user' ? 'Choose Your Opponent' : 'Select First Debater'}
          </h2>
          <div className="grid md:grid-cols-2 gap-4">
            {historicalFigures.map(figure => (
              <button
                key={figure.id}
                onClick={() => handleFigureSelect(figure)}
                className="bg-white/10 backdrop-blur-sm p-4 rounded-lg hover:bg-white/20 transition-colors text-left"
              >
                <h3 className="font-bold text-lg">{figure.name}</h3>
                <p className="text-gray-300">{figure.period}</p>
              </button>
            ))}
          </div>
        </div>
      )}

      {selectedFigure && debateMode === 'ai' && !selectedOpponent && (
        <div className="space-y-4">
          <h2 className="text-2xl font-bold">Select Second Debater</h2>
          <div className="grid md:grid-cols-2 gap-4">
            {historicalFigures
              .filter(figure => figure.id !== selectedFigure.id)
              .map(figure => (
                <button
                  key={figure.id}
                  onClick={() => handleFigureSelect(figure)}
                  className="bg-white/10 backdrop-blur-sm p-4 rounded-lg hover:bg-white/20 transition-colors text-left"
                >
                  <h3 className="font-bold text-lg">{figure.name}</h3>
                  <p className="text-gray-300">{figure.period}</p>
                </button>
              ))}
          </div>
        </div>
      )}

      {((debateMode === 'user' && selectedFigure) || (debateMode === 'ai' && selectedFigure && selectedOpponent)) && !selectedTopic && (
        <div className="space-y-4">
          <h2 className="text-2xl font-bold">Choose a Debate Topic</h2>
          <div className="grid md:grid-cols-2 gap-4">
            {debateTopics.map(topic => (
              <button
                key={topic.id}
                onClick={() => handleTopicSelect(topic)}
                className="bg-white/10 backdrop-blur-sm p-4 rounded-lg hover:bg-white/20 transition-colors text-left"
              >
                <h3 className="font-bold text-lg">{topic.title}</h3>
                <p className="text-gray-300">{topic.description}</p>
              </button>
            ))}
          </div>
        </div>
      )}

      {selectedFigure && selectedTopic && (
        <div className="space-y-4">
          <div className="bg-white/10 backdrop-blur-sm p-4 rounded-lg">
            <h2 className="text-xl font-bold mb-2">
              {debateMode === 'user' 
                ? `Debating with ${selectedFigure.name}`
                : `Debate between ${selectedFigure.name} and ${selectedOpponent?.name}`
              } about {selectedTopic.title}
            </h2>
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {debate.map((entry, index) => (
                <div
                  key={index}
                  className={`p-3 rounded-lg ${
                    entry.speaker === 'You'
                      ? 'bg-purple-600/20 ml-8'
                      : entry.speaker === selectedFigure.name
                      ? 'bg-blue-600/20 mr-8'
                      : 'bg-green-600/20 ml-8'
                  }`}
                >
                  <div className="font-semibold mb-1">{entry.speaker}</div>
                  <div>{entry.text}</div>
                </div>
              ))}
            </div>
          </div>

          {debateMode === 'user' && (
            <div className="flex gap-4">
              <input
                type="text"
                value={userArgument}
                onChange={(e) => setUserArgument(e.target.value)}
                placeholder="Type your argument..."
                className="flex-1 bg-white/5 backdrop-blur-sm rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
              />
              <button
                onClick={handleSubmitArgument}
                className="bg-purple-600 hover:bg-purple-700 px-6 py-2 rounded-lg transition-colors"
              >
                Submit
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default DebateSimulator;