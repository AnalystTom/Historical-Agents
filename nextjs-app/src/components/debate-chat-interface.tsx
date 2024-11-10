'use client'

import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Debater, Message } from '@/types'
import { Mic, User } from 'lucide-react'

interface DebateChatInterfaceProps {
  gameMode: string
  topic: string
  debaters: Debater[]
}

export function DebateChatInterface({ gameMode, topic, debaters }: DebateChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([])
  const [inputMessage, setInputMessage] = useState('')
  const [isConnected, setIsConnected] = useState(false)
  const [currentTurn, setCurrentTurn] = useState<string>(debaters[0].id)
  const scrollAreaRef = useRef<HTMLDivElement>(null)
  const ws = useRef<WebSocket | null>(null)

  useEffect(() => {
    // WebSocket connection logic (unchanged)
    // ...

    // Add some initial messages for testing
    setMessages([
      { id: '1', sender: 'system', content: `Welcome to the debate on "${topic}"`, timestamp: new Date() },
      { id: '2', sender: debaters[0].id, content: 'Thank you for having me. I\'m ready to begin the debate.', timestamp: new Date() },
      { id: '3', sender: debaters[1]?.id || 'user', content: 'I appreciate the opportunity to discuss this important topic.', timestamp: new Date() },
    ])

    return () => {
      ws.current?.close()
    }
  }, [gameMode, topic, debaters])

  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight
    }
  }, [messages])

  const handleSendMessage = () => {
    if (inputMessage.trim() && isConnected) {
      const newMessage: Message = {
        id: Date.now().toString(),
        sender: gameMode === 'you-vs-ai' ? 'user' : 'moderator',
        content: inputMessage,
        timestamp: new Date()
      }
      setMessages((prevMessages) => [...prevMessages, newMessage])
      ws.current?.send(JSON.stringify(newMessage))
      setInputMessage('')
      
      // Switch turns
      setCurrentTurn(currentTurn === debaters[0].id ? debaters[1].id : debaters[0].id)
    }
  }

  const getDebaterByName = (name: string) => debaters.find(d => d.id === name) || debaters[0]

  return (
    <div className="min-h-screen bg-cover bg-center" style={{backgroundImage: "url('/debate-stage.jpg')"}}>
      <Card className="w-full max-w-4xl mx-auto bg-black/70 text-white">
        <CardHeader>
          <CardTitle className="text-2xl font-bold text-center">
            {gameMode === 'ai-vs-ai' ? 'AI vs AI Debate' : 'You vs AI Debate'}
          </CardTitle>
          <p className="text-center text-gray-300">Topic: {topic}</p>
        </CardHeader>
        <CardContent>
          <div className="flex justify-between mb-4">
            {debaters.map((debater) => (
              <div key={debater.id} className="flex flex-col items-center">
                <Avatar className="w-16 h-16">
                  <AvatarImage src={debater.image} alt={debater.name} />
                  <AvatarFallback>{debater.name[0]}</AvatarFallback>
                </Avatar>
                <span className="mt-2 font-semibold">{debater.name}</span>
                {currentTurn === debater.id && (
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ duration: 0.3 }}
                    className="mt-2 bg-green-500 text-white px-2 py-1 rounded-full text-xs"
                  >
                    Speaking
                  </motion.div>
                )}
              </div>
            ))}
          </div>
          <ScrollArea className="h-[60vh] mb-4 pr-4" ref={scrollAreaRef}>
            <AnimatePresence initial={false}>
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, transition: { duration: 0.2 } }}
                  className="mb-4"
                >
                  <div className={`flex ${message.sender === 'user' || message.sender === 'moderator' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`flex items-start max-w-[80%] ${message.sender === 'user' || message.sender === 'moderator' ? 'flex-row-reverse' : 'flex-row'}`}>
                      <Avatar className="w-8 h-8">
                        {message.sender === 'user' || message.sender === 'moderator' ? (
                          <User className="w-6 h-6" />
                        ) : (
                          <AvatarImage src={getDebaterByName(message.sender).image} alt={getDebaterByName(message.sender).name} />
                        )}
                      </Avatar>
                      <div 
                        className={`mx-2 p-3 rounded-lg ${
                          message.sender === 'user' || message.sender === 'moderator'
                            ? 'bg-blue-500 text-white' 
                            : message.sender === 'system'
                            ? 'bg-gray-500 text-white'
                            : 'bg-gray-200 text-black'
                        }`}
                      >
                        <p className="font-semibold mb-1">
                          {message.sender === 'user' ? 'You' : 
                           message.sender === 'moderator' ? 'Moderator' : 
                           message.sender === 'system' ? 'System' :
                           getDebaterByName(message.sender).name}
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
          <div className="flex items-center mt-4">
            <Input
              type="text"
              placeholder={gameMode === 'you-vs-ai' ? "Your argument..." : "Ask a question..."}
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              className="flex-grow mr-2 bg-gray-700 text-white placeholder-gray-400"
            />
            <Button onClick={handleSendMessage} disabled={!isConnected} className="bg-blue-500 hover:bg-blue-600">
              {gameMode === 'you-vs-ai' ? <Mic className="mr-2" /> : null}
              {gameMode === 'you-vs-ai' ? 'Speak' : 'Send'}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}