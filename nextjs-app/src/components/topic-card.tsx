import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card"
import { motion } from "framer-motion"
import { Topic } from "@/types"

interface TopicCardProps {
  topic: Topic
  isSelected: boolean
  onSelect: () => void
}

export function TopicCard({ topic, isSelected, onSelect }: TopicCardProps) {
  return (
    <motion.div
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
    >
      <Card 
        className={`cursor-pointer transition-colors duration-200 ${
          isSelected ? 'bg-primary text-primary-foreground' : 'bg-card hover:bg-card/80'
        }`}
        onClick={onSelect}
      >
        <CardHeader>
          <CardTitle>{topic.title}</CardTitle>
          <CardDescription className={isSelected ? 'text-primary-foreground' : ''}>
            {topic.category}
          </CardDescription>
        </CardHeader>
      </Card>
    </motion.div>
  )
}