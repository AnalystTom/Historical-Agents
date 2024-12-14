"use client";

import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { DebateChatInterface } from "@/components/debate-chat-interface";
import { Debater, Message } from "@/types";

export default function DebatePage() {
  const searchParams = useSearchParams();
  const debate_topic = searchParams.get("debate_topic");
  const debater1 = searchParams.get("debater1");
  const debater2 = searchParams.get("debater2");

  const [greetings, setGreetings] = useState<string>("Welcome to the debate!");
  const [conversation, setConversation] = useState<Message[]>([]);
  const [winner, setWinner] = useState<string>(""); // Updated dynamically
  const [debateHistory, setDebateHistory] = useState<string[]>([]); // Stores debate summary

  const debater1Id = debater1 || "unknown";
  const debater2Id = debater2 || "unknown";

  useEffect(() => {
    if (!debate_topic || !debater1 || !debater2) return;

    const ws = new WebSocket("ws://localhost:8000/ws/debate");

    ws.onopen = () => {
      console.log("WebSocket connection established");
      ws.send(
        JSON.stringify({
          topic: debate_topic,
          pro_debator: debater1,
          anti_debator: debater2,
          max_iterations: 2,
        })
      );
    };

    ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);

        if (message.type === "new_message" && message.data) {
          const { type: messageType, message: messageContent } = message.data;

          setConversation((prev) => {
            console.log("Received new_message: ", message);

            const senderName =
              messageType === "HumanMessage"
                ? `${debater1}`
                : messageType === "AIMessage"
                ? `${debater2}`
                : "system";

            const updatedConversation = [
              ...prev,
              {
                id: `${prev.length}`,
                sender: senderName,
                content: messageContent,
                timestamp: new Date(),
              },
            ];
            return updatedConversation;
          });
        } else if (message.type === "final_result") {
          console.log("Received final_result: ", message);

          // Update winner and debate history
          setWinner(message.winner.winner || "No winner decided");
          setDebateHistory([
            `Summary: ${message.summary || "No summary available"}`,
            `Clarity: ${message.winner.clarity}`,
            `Persuasiveness: ${message.winner.persuasiveness}`,
            `Relevance: ${message.winner.relevance}`,
            `Logical Soundness: ${message.winner.logical_soundness}`,
          ]);
        } else {
          console.warn("Unexpected WebSocket message format:", message);
        }
      } catch (error) {
        console.error("Error parsing WebSocket message:", error);
      }
    };

    ws.onclose = () => {
      console.log("WebSocket connection closed");
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    return () => {
      ws.close();
    };
  }, [debate_topic, debater1, debater2]);

  useEffect(() => {
    console.log("Conversation state updated:", conversation);
  }, [conversation]);

  const debaters: Debater[] = [
    {
      id: debater1Id,
      name: debater1Id,
      image: "/debater1.jpg",
      yearsActive: "Unknown",
      quote: "No quote available",
      achievements: [],
      background: "No background available",
      tone: "Neutral",
      style: "Formal",
    },
    {
      id: debater2Id,
      name: debater2Id,
      image: "/debater2.jpg",
      yearsActive: "Unknown",
      quote: "No quote available",
      achievements: [],
      background: "No background available",
      tone: "Neutral",
      style: "Formal",
    },
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      <DebateChatInterface
        gameMode="ai-vs-ai"
        topic={debate_topic || "Unknown Topic"}
        debaters={debaters}
        messages={conversation}
        winner={winner} // Pass the winner to the interface
        history={debateHistory} // Pass the debate history
      />
    </div>
  );
}
