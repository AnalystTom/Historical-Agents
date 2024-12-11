'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Button } from "@/components/ui/button"
import { DebaterCard } from '@/components/debater-card'
import { Debater } from '@/types'
import { useRouter } from 'next/navigation'; // Correct import for App Router

const debaters: Debater[] = [
    {
      id: 'Benjamin Netanyahu',
      name: 'Benjamin Netanyahu',
      image: '/netanyahu.jpg',
      yearsActive: '1949-Present',
      quote: "If the Arabs put down their weapons today, there would be no more violence. If the Jews put down their weapons today, there would be no more Israel.",
      achievements: [
        'Longest-serving PM of Israel',
        'Economic Reforms',
        'Middle East Peace Agreements'
      ],
      background: 'Former Prime Minister of Israel',
      tone: 'Assertive and unyielding',
      style: 'Strategic and diplomatic'
    },
    {
      id: 'Norman Finkelstein',
      name: 'Norman Finkelstein',
      image: '/finkelstein.jpg',
      yearsActive: '1953-Present',
      quote: "I don't believe in intellectual property. Knowledge should be free and shared.",
      achievements: [
        'Political Scientist',
        'Human Rights Activist',
        'Published Author'
      ],
      background: 'American political scientist and activist',
      tone: 'Academic and confrontational',
      style: 'Analytical and critical'
    },
    {
      id: 'vladimir-putin',
      name: 'Vladimir Putin',
      image: '/putin.jpg',
      yearsActive: '1952-Present',
      quote: "The collapse of the Soviet Union was a major geopolitical disaster of the century.",
      achievements: [
        'President of Russia',
        'Former KGB Officer',
        'Economic Reformer'
      ],
      background: 'President of Russia',
      tone: 'Authoritative and calculated',
      style: 'Strategic and assertive'
    }
  ]



export default function DebaterSelection() {
  const [selectedDebaters, setSelectedDebaters] = useState<string[]>([]);
  const [customDebater1, setCustomDebater1] = useState<string>('');
  const [customDebater2, setCustomDebater2] = useState<string>('');
  const [gameMode, setGameMode] = useState<string | null>(null);
  const [topic, setTopic] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    const storedGameMode = localStorage.getItem('selectedGameMode');
    const storedTopic = localStorage.getItem('selectedTopic');
    if (!storedGameMode || !storedTopic) {
      console.log('Missing game mode or topic, redirecting to home...');
      router.push('/');
    } else {
      setGameMode(storedGameMode);
      setTopic(storedTopic);
      console.log(`Game mode: ${storedGameMode}, Topic: ${storedTopic}`);
    }
  }, [router]);

  const handleDebaterSelect = (debaterId: string) => {
    setSelectedDebaters(prev => {
      if (prev.includes(debaterId)) {
        return prev.filter(id => id !== debaterId);
      } else if (gameMode === 'ai-vs-ai' && prev.length < 2) {
        return [...prev, debaterId];
      } else if (gameMode === 'you-vs-ai' && prev.length < 1) {
        return [debaterId];
      }
      return prev;
    });
  };

  const handleContinue = () => {
    const debatersToUse = customDebater1 && customDebater2 ? [customDebater1, customDebater2] : selectedDebaters;
    if ((gameMode === 'ai-vs-ai' && debatersToUse.length === 2) || 
        (gameMode === 'you-vs-ai' && debatersToUse.length === 1)) {
      console.log('Selected debaters:', debatersToUse);
      localStorage.setItem('selectedDebaters', JSON.stringify(debatersToUse));
      const queryString = `debate_topic=${encodeURIComponent(topic || '')}&debater1=${encodeURIComponent(debatersToUse[0])}&debater2=${encodeURIComponent(debatersToUse[1] || '')}`;
      router.push(`/debate-interface?${queryString}`);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 flex flex-col items-center justify-center p-4">
      <motion.h1 
        className="text-4xl md:text-5xl font-serif mb-4 text-center"
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        Select Two Debaters
      </motion.h1>
      <motion.p
        className="text-xl mb-8 text-center"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3, duration: 0.5 }}
      >
        Topic: {topic}
      </motion.p>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-16 w-full max-w-4xl mx-auto mb-8 text-center">
        {debaters.map((debater) => (
          <DebaterCard
            key={debater.id}
            debater={debater}
            isSelected={selectedDebaters.includes(debater.id)}
            onSelect={() => handleDebaterSelect(debater.id)}
          />
        ))}
      </div>
      <p className="text-xl mb-4 text-center">Or choose your own:</p>
      <div className="flex space-x-4 mb-8 justify-center">
        <input
          type="text"
          placeholder="Input Pro Debater"
          value={customDebater1}
          onChange={(e) => setCustomDebater1(e.target.value)}
          className="p-2 bg-gray-800 text-white rounded border-2 border-gray-700"
        />
        <input
          type="text"
          placeholder="Input Anti Debater"
          value={customDebater2}
          onChange={(e) => setCustomDebater2(e.target.value)}
          className="p-2 bg-gray-800 text-white rounded border-2 border-gray-700"
        />
      </div>
      <motion.div
        className="mt-8"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        <Button 
          size="lg" 
          onClick={handleContinue}
          className={`p-2 rounded border-2 ${selectedDebaters.length === 2 || (customDebater1 && customDebater2) ? 'bg-gray-800 text-white border-gray-700' : ''}`}
          disabled={(gameMode === 'ai-vs-ai' && selectedDebaters.length !== 2 && (!customDebater1 || !customDebater2)) || 
                    (gameMode === 'you-vs-ai' && selectedDebaters.length !== 1 && !customDebater1)}
        >
          Start Debate
        </Button>
      </motion.div>
    </div>
  );
}