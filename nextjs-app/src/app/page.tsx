'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { motion } from 'framer-motion'
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { UserIcon, Users } from 'lucide-react'

const gameModes = [
  { 
    id: 'ai-vs-ai', 
    name: 'AI vs AI', 
    description: 'Moderate the debate by asking questions',
    icon: Users
  },
  { 
    id: 'you-vs-ai', 
    name: 'You vs AI', 
    description: 'Debate figures on the specific topic',
    icon: UserIcon
  },
]

export default function GameModeSelection() {
  const [selectedMode, setSelectedMode] = useState<string | null>(null)
  const router = useRouter()

  const handleModeSelect = (modeId: string) => {
    setSelectedMode(modeId)
  }

  const handleContinue = () => {
    if (selectedMode) {
      localStorage.setItem('selectedGameMode', selectedMode)
      router.push('/topic-selection')
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 flex flex-col items-center justify-center p-4" style={{backgroundImage: "url('/parchment-dark.jpg')"}}>
      <motion.h1 
        className="text-4xl md:text-5xl font-serif mb-8 text-center"
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        Choose Your Debate Mode
      </motion.h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-4xl">
        {gameModes.map((mode) => (
          <motion.div
            key={mode.id}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Card 
              className={`cursor-pointer transition-colors duration-200 ${
                selectedMode === mode.id ? 'bg-primary text-primary-foreground' : 'bg-card hover:bg-card/80'
              }`}
              onClick={() => handleModeSelect(mode.id)}
            >
              <CardHeader className="flex flex-col items-center text-center">
                <mode.icon className="w-12 h-12 mb-4" />
                <CardTitle>{mode.name}</CardTitle>
                <CardDescription className={selectedMode === mode.id ? 'text-primary-foreground' : ''}>
                  {mode.description}
                </CardDescription>
              </CardHeader>
            </Card>
          </motion.div>
        ))}
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
          disabled={!selectedMode}
        >
          Continue to Topic Selection
        </Button>
      </motion.div>
    </div>
  )
}