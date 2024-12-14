export type GameMode = "ai-vs-ai" | "you-vs-ai";

export type Topic = {
  id: string;
  title: string;
  category: string;
};

export type Debater = {
  id: string;
  name: string;
  image: string;
  yearsActive: string;
  quote: string;
  achievements: string[];
  background: string;
  tone: string;
  style: string;
};

export type Message = {
  id: string;
  sender: string;
  content: string;
  timestamp: Date;
};

export interface DebateChatInterfaceProps {
  gameMode: string;
  topic: string; // Add this line if it's missing
  debaters: Debater[];
  messages: Message[];
}
