'use client'

import { useState, useEffect } from 'react';
import { DebateChatInterface } from '@/components/debate-chat-interface';
import { Debater, Message } from '@/types';

export default function DebatePage() {
  const [greetings, setGreetings] = useState<string>('');
  const [conversation, setConversation] = useState<Message[]>([]);
  const [debateHistory, setDebateHistory] = useState<string[]>([]);
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    const fetchDebateData = async () => {
      try {
        const response = await fetch('http://localhost:8000/trigger_workflow', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            debate_topic: 'AI in Football?',
            debater1: 'benjamin-netanyahu',
            debater2: 'yair-lapid',
            max_iterations: 3
          })
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        setGreetings(data.greetings);
        setConversation(data.conversation.map((msg: any, index: number) => ({
          id: index.toString(),
          sender: msg.speaker,
          content: msg.content,
          timestamp: new Date()
        })));
        setDebateHistory(data.debate_history);
        setIsReady(true);
      } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
      }
    };

    fetchDebateData();
  }, []);

  if (!isReady) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <p className="text-2xl font-bold">Loading debate...</p>
      </div>
    );
  }

  const debaters: Debater[] = [
    { id: 'benjamin-netanyahu', name: 'Benjamin Netanyahu', image: '/benjamin-netanyahu.jpg' },
    { id: 'yair-lapid', name: 'Yair Lapid', image: '/yair-lapid.jpg' }
  ];

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <h1 className="text-2xl font-bold mb-4">Debate Session</h1>
      <div className="mb-4">
        <p className="font-bold">Greetings:</p>
        <p>{greetings}</p>
      </div>
      <DebateChatInterface 
        gameMode="ai-vs-ai"
        topic="AI in Football?"
        debaters={debaters}
        messages={conversation}
      />
      <div>
        <p className="font-bold">Debate History:</p>
        {debateHistory.map((history, index) => (
          <p key={index} className="bg-gray-200 p-2 rounded mb-2">{history}</p>
        ))}
      </div>
    </div>
  );
}