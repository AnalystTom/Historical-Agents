'use client'

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation'; // Correct import
import { DebateChatInterface } from '@/components/debate-chat-interface';
import { Debater, Message } from '@/types';

export default function DebatePage() {
  const searchParams = useSearchParams(); // Use useSearchParams
  const debate_topic = searchParams.get('debate_topic');
  const debater1 = searchParams.get('debater1');
  const debater2 = searchParams.get('debater2');
  
  const [greetings, setGreetings] = useState<string>('');
  const [conversation, setConversation] = useState<Message[]>([]);
  const [debateHistory, setDebateHistory] = useState<string[]>([]);
  const [debateWinner, setWinner] = useState<string>('');
  const [isReady, setIsReady] = useState(false);
  const debater1Id = debater1 || 'unknown';
  const debater2Id = debater2 || 'unknown';

  useEffect(() => {
    if (!debate_topic || !debater1 || !debater2) return; // Ensure parameters are available

    const fetchDebateData = async () => {
      try {
        const response = await fetch('http://localhost:8000/trigger_workflow', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            debate_topic,
            debater1,
            debater2,
            max_iterations: 2
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
          content: formatContent(msg.content),
          timestamp: new Date()
        })));
        setWinner(formatContent(data.winner)); // Format the winner content
        setDebateHistory(data.debate_history.filter((entry: string) => !entry.includes('Summarizer'))); // Filter out summarizer
      setIsReady(true);
      } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
      }
    };

    fetchDebateData();
  }, [debate_topic, debater1, debater2]);

  const formatContent = (content: string) => {
    // Use regular expressions to insert newlines before specific patterns
    return content
      .replace(/(\d+\))/g, '\n$1') // Inserts a newline before each numbered point
      .replace(/(Main Points of Disagreement, \d+)/g, '\n$1')
      .replace(/(Objective Overview)/g, '\n$1')
      .replace(/(Main Points of Agreement, \d+)/g, '\n$1');
  };

  if (!isReady) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <p className="text-2xl font-bold">Loading debate...</p>
      </div>
    );
  }

  const debaters: Debater[] = [
    {
      id: debater1Id,
      name: debater1Id,
      image: '/debater1.jpg',
      yearsActive: 'Unknown',
      quote: 'No quote available',
      achievements: [],
      background: 'No background available',
      tone: 'Neutral',
      style: 'Formal'
    },
    {
      id: debater2Id,
      name: debater2Id,
      image: '/debater2.jpg',
      yearsActive: 'Unknown',
      quote: 'No quote available',
      achievements: [],
      background: 'No background available',
      tone: 'Neutral',
      style: 'Formal'
    }
  ];

  const combinedMessages: Message[] = [
    { id: 'greeting', sender: 'system', content: greetings, timestamp: new Date() },
    ...conversation,
    ...debateHistory.map((history, index) => ({
      id: `history-${index}`,
      sender: 'system',
      content: history,
      timestamp: new Date()
    })),
    { id: 'winner', sender: 'system', content: debateWinner, timestamp: new Date() } // Add winner to messages
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      <DebateChatInterface 
        gameMode="ai-vs-ai"
        topic={debate_topic}
        debaters={debaters}
        messages={combinedMessages}
     />
    </div>
  )
}