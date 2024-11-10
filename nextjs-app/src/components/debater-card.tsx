import { Card, CardHeader, CardContent } from "@/components/ui/card"
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar"
import { motion } from "framer-motion"
import { Debater } from "@/types"

interface DebaterCardProps {
  debater: Debater
  isSelected: boolean
  onSelect: () => void
}

export function DebaterCard({ debater, isSelected, onSelect }: DebaterCardProps) {
  return (
    <motion.div
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
    >
      <Card 
        className={`cursor-pointer transition-colors duration-200 h-[500px] w-[300px] flex flex-col ${
          isSelected ? 'bg-primary text-primary-foreground' : 'bg-card hover:bg-card/80'
        }`}
        onClick={onSelect}
      >
        <CardHeader className="flex-shrink-0 flex flex-col items-center text-center space-y-4">
          <Avatar className="w-24 h-24">
            <AvatarImage src={debater.image} alt={debater.name} />
            <AvatarFallback className="text-2xl">
              {debater.name.split(' ').map(n => n[0]).join('')}
            </AvatarFallback>
          </Avatar>
          <div className="space-y-1">
            <h3 className="text-2xl font-bold">{debater.name}</h3>
            <p className="text-sm text-muted-foreground">
              {debater.yearsActive}
            </p>
          </div>
        </CardHeader>
        <CardContent className="text-center space-y-4 flex-grow overflow-auto">
          <blockquote className="italic text-sm border-l-4 pl-4 mx-4">
            "{debater.quote}"
          </blockquote>
          <ul className="space-y-2">
            {debater.achievements.map((achievement, index) => (
              <li 
                key={index}
                className={`text-sm py-1 px-3 rounded-full ${
                  isSelected 
                    ? 'bg-primary-foreground/20 text-primary-foreground' 
                    : 'bg-muted text-muted-foreground'
                }`}
              >
                {achievement}
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </motion.div>
  )
}