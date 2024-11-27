import { BotMessageSquare, History, Book, Users, Globe, Lightbulb } from "lucide-react";

export const navItems = [
  { label: "Overview", href: "#workflow" },
  { label: "Features", href: "#features" },
  { label: "Debate Modes", href: "/ideas" },
];

export const features = [
  {
    icon: <BotMessageSquare />,
    text: "AI-Powered Debates",
    description: "Experience AI-driven debates where virtual historical figures engage in insightful, complex discussions.",
  },
  {
    icon: <History />,
    text: "Interactive Timeline",
    description: "Track the flow of arguments and key points through an interactive timeline, making debates easy to follow.",
  },
  {
    icon: <Book />,
    text: "Educational Topics",
    description: "Explore debates on predefined topics, from philosophy to politics, tailored for learning and intellectual growth.",
  },
  {
    icon: <Users />,
    text: "User vs AI Mode",
    description: "Engage in debates directly with AI-powered historical figures, challenging your perspectives in real-time.",
  },
  {
    icon: <Globe />,
    text: "Global Perspectives",
    description: "Discover diverse viewpoints by debating figures from various cultures and backgrounds.",
  },
  {
    icon: <Lightbulb />,
    text: "Curated Topics and Figures",
    description: "Choose from carefully selected figures and debate topics designed to inspire and educate.",
  },
];

export const checklistItems = [
  {
    title: "Engaging AI-Driven Debates",
    description:
      "Immerse yourself in debates moderated by AI, allowing you to witness virtual discussions on complex issues.",
  },
  {
    title: "Interactive Debate Timeline",
    description: "Easily follow the progression of arguments with an interactive timeline that highlights key moments.",
  },
  {
    title: "Diverse Debate Topics",
    description: "Choose from a range of intellectually stimulating topics such as philosophy and global politics.",
  },
  {
    title: "Historic and Cultural Figures",
    description: "Debate or moderate discussions featuring renowned figures from various historical and cultural backgrounds.",
  },
];

export const resourcesLinks = [
  { href: "#", text: "Getting Started" },
  { href: "#", text: "User Guide" },
  { href: "#", text: "Debate Tips" },
  { href: "#", text: "AI Explanation" },
  { href: "#", text: "FAQ" },
];

export const platformLinks = [
  { href: "#", text: "Features" },
  { href: "#", text: "Supported Browsers" },
  { href: "#", text: "System Requirements" },
  { href: "#", text: "Updates" },
  { href: "#", text: "Release Notes" },
];

export const communityLinks = [
  { href: "#", text: "Events" },
  { href: "#", text: "Webinars" },
  { href: "#", text: "Forums" },
  { href: "#", text: "Workshops" },
  { href: "#", text: "Join Community" },
];
