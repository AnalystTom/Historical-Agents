'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { Button } from "@/components/ui/button"
import { TopicCard } from '@/components/topic-card'
import { Topic } from '@/types'

const topics: Topic[] = [
  { id: 'israel-palestine', title: 'Israel-Palestine Conflict', category: 'Politics' },
  { id: 'existence-of-god', title: 'Existence of God', category: 'Philosophy' },
]

export default function TopicSelection() {
  const [selectedTopic, setSelectedTopic] = useState<string | null>(null);
  const [customTopic, setCustomTopic] = useState<string>('');
  const router = useRouter();

  useEffect(() => {
    // Set the default game mode to "AI vs AI"
    localStorage.setItem('selectedGameMode', 'ai-vs-ai');
  }, []);

  const handleSelect = (topicId: string) => {
    setSelectedTopic((prevSelectedTopic) => 
      prevSelectedTopic === topicId ? null : topicId
    );
  };

  const handleContinue = () => {
    const topicToUse = customTopic || selectedTopic;
    if (topicToUse) {
      localStorage.setItem('selectedTopic', topicToUse);
      router.push('/debater-selection');
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 flex flex-col items-center justify-center p-4">
      <motion.h1 
        className="text-4xl md:text-5xl font-serif mb-8 text-center"
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        Select a Topic
      </motion.h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-4xl mb-8">
        {topics.map((topic) => (
          <TopicCard
            key={topic.id}
            topic={topic}
            isSelected={selectedTopic === topic.id}
            onSelect={() => handleSelect(topic.id)}
          />
        ))}
      </div>
      <p className="text-xl mb-4 text-center">Or enter your own topic:</p>
      <div className="flex space-x-4 mb-8 justify-center">
        <input
          type="text"
          placeholder="Input Custom Topic"
          value={customTopic}
          onChange={(e) => setCustomTopic(e.target.value)}
          className="p-2 bg-gray-800 text-white rounded border-2 border-gray-700"
        />
      </div>
      <motion.div
        className="mt-2"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        <Button 
          size="lg" 
          onClick={handleContinue}
          className={`p-2 rounded border-2 ${selectedTopic || customTopic ? 'bg-gray-800 text-white border-gray-700' : ''}`}
          disabled={!selectedTopic && !customTopic}
        >
          Continue to Debater Selection
        </Button>
      </motion.div>
    </div>
  );
}