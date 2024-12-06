'use client';

import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Debater, Message } from '@/types';
import { Mic, User } from 'lucide-react';

interface DebateChatInterfaceProps {
  gameMode: string;
  topic: string;
  debaters: Debater[];
  messages: Message[];
}

export function DebateChatInterface({ gameMode, topic, debaters, messages }: DebateChatInterfaceProps) {
  const [inputMessage, setInputMessage] = useState('');
  const [isConnected, setIsConnected] = useState(false);
  const [currentTurn, setCurrentTurn] = useState<string>(debaters[0].id);
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const ws = useRef<WebSocket | null>(null);

  const capitalizeName = (name: string) => {
    return name.replace(/\b\w/g, (char) => char.toUpperCase());
  };

  const getDebaterByName = (name: string) => {
    return debaters.find((d) => d.id === name) || debaters[0];
  };

  const handleSendMessage = () => {
    if (inputMessage.trim() && isConnected) {
      const newMessage: Message = {
        id: Date.now().toString(),
        sender: gameMode === 'you-vs-ai' ? 'user' : 'moderator',
        content: inputMessage,
        timestamp: new Date(),
      };
      ws.current?.send(JSON.stringify(newMessage));
      setInputMessage('');

      // Switch turns
      setCurrentTurn(currentTurn === debaters[0].id ? debaters[1].id : debaters[0].id);
    }
  };

  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = 0; // Scroll to the top when the component mounts
    }
  }, []); // Empty dependency array to run only on mount

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 flex flex-col items-center justify-start p-4 overflow-hidden">
      <Card className="w-full mx-auto bg-transparent text-white border-none shadow-none">
        <CardHeader>
          <CardTitle className="text-4xl md:text-5xl font-serif text-center mb-2">
            {gameMode === 'ai-vs-ai' ? 'AI vs AI Debate' : 'You vs AI Debate'}
          </CardTitle>
          <p className="text-center text-gray-300 mb-4">Topic: {topic}</p>
        </CardHeader>
        <CardContent>
          <div className="flex justify-between mb-4">
            {/* Debater avatars and turn indicator */}
          </div>
          <ScrollArea className="h-[80vh] mb-4 pr-4" ref={scrollAreaRef}>
            <AnimatePresence initial={false}>
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, transition: { duration: 0.2 } }}
                  className="mb-4"
                >
                  <div
                    className={`flex ${
                      message.sender === 'system'
                        ? 'justify-center'
                        : message.sender === debaters[0].id
                        ? 'justify-start'
                        : 'justify-end'
                    }`}
                  >
                    <div
                      className={`flex items-start max-w-[80%] ${
                        message.sender === debaters[0].id ? 'flex-row' : 'flex-row-reverse'
                      }`}
                    >
                      <Avatar className="w-8 h-8">
                        {message.sender === 'system' ? (
                          <User className="w-6 h-6" />
                        ) : (
                          <AvatarImage
                            src={getDebaterByName(message.sender).image}
                            alt={getDebaterByName(message.sender).name}
                          />
                        )}
                      </Avatar>
                      <div
                        className={`mx-2 p-3 rounded-lg ${
                          message.sender === 'system'
                            ? 'bg-gray-500 text-white'
                            : message.sender === debaters[0].id
                            ? 'bg-blue-500 text-white'
                            : 'bg-gray-200 text-black'
                        }`}
                      >
                        <p className="font-semibold mb-1">
                          {message.sender === 'system'
                            ? 'System'
                            : getDebaterByName(message.sender).name}
                        </p>
                        <p>{message.content}</p>
                        <span className="text-xs opacity-70 mt-1 block">
                          {new Date(message.timestamp).toLocaleTimeString()}
                        </span>
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          </ScrollArea>
        </CardContent>
      </Card>
    </div>
  );
}