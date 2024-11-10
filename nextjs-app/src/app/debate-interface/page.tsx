'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { DebateChatInterface } from '@/components/debate-chat-interface'
import { Debater } from '@/types'

export default function DebatePage() {
  const [gameMode, setGameMode] = useState<string | null>(null)
  const [topic, setTopic] = useState<string | null>(null)
  const [debaters, setDebaters] = useState<Debater[]>([])
  const [isReady, setIsReady] = useState(false)
  const router = useRouter()

  useEffect(() => {
    const storedGameMode = localStorage.getItem('selectedGameMode')
    const storedTopic = localStorage.getItem('selectedTopic')
    const storedDebaters = JSON.parse(localStorage.getItem('selectedDebaters') || '[]')

    console.log('Stored data:', { storedGameMode, storedTopic, storedDebaters })

    if (!storedGameMode || !storedTopic || storedDebaters.length === 0) {
      console.log('Missing data, redirecting to home')
      router.push('/')
    } else {
      setGameMode(storedGameMode)
      setTopic(storedTopic)
      // For simplicity, we're using the debater IDs as the full debater objects.
      // In a real application, you'd fetch the full debater details here.
      setDebaters(storedDebaters.map((id: string) => ({ id, name: id, image: `/placeholder.svg?height=100&width=100` })))
      setIsReady(true)
    }
  }, [router])

  if (!isReady) {
    return <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <p className="text-2xl font-bold">Loading debate...</p>
    </div>
  }

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <DebateChatInterface 
        gameMode={gameMode!}
        topic={topic!}
        debaters={debaters}
      />
    </div>
  )
}