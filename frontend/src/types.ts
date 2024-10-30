export type GameMode = 'guessing' | 'debate';

export interface HistoricalFigure {
  id: string;
  name: string;
  period: string;
  facts: string[];
  hints: string[];
  image: string;
}

export interface DebateTopic {
  id: string;
  title: string;
  description: string;
  period: string;
  perspectives: Record<string, string[]>;
}

export interface GameState {
  questionsAsked: number;
  currentScore: number;
  isGameOver: boolean;
}