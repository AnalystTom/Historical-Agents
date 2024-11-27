import { useState, useEffect } from "react";
import { getButtonClass } from "../components/Button";
import { generateIdeas } from "../Services/ideaGenService";
import { setAuthToken } from "../Services/api";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import sanitizeHtml from "sanitize-html";

const IdeaGenerator = () => {
  const [step, setStep] = useState(1);
  const [mode, setMode] = useState("");
  const [topic, setTopic] = useState("");
  const [selectedFigures, setSelectedFigures] = useState([]);
  const [inputValue, setInputValue] = useState("");
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const bearerToken = "bearer_token_here";

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSubmit = async () => {
    if (!inputValue.trim()) return;

    // Add the user's message to the conversation
    const userMessage = { sender: "user", text: inputValue };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    setInputValue(""); // Clear the input field

    setIsLoading(true); // Start loading

    try {
      // Simulate AI response
      const aiResponse = `${selectedFigures[0]}: This is a simulated response to your message.`;

      // Wait for a moment to simulate delay
      await new Promise((resolve) => setTimeout(resolve, 1000));

      const assistantMessage = { sender: "assistant", text: aiResponse };
      setMessages((prevMessages) => [...prevMessages, assistantMessage]);
    } catch (error) {
      console.error("Failed to get response:", error);
      const errorMessage = { sender: "assistant", text: "Failed to get response. Please try again." };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false); // End loading
    }
  };

  const startAIDebate = () => {
    const [figure1, figure2] = selectedFigures;
    let turn = 0;
    const maxTurns = 5; // Number of exchanges

    const debateInterval = setInterval(() => {
      if (turn >= maxTurns) {
        clearInterval(debateInterval);
        return;
      }
      const speaker = turn % 2 === 0 ? figure1 : figure2;
      const message = `${speaker}: This is a simulated response for turn ${turn + 1}.`;
      setMessages((prevMessages) => [...prevMessages, { sender: "assistant", text: message }]);
      turn++;
    }, 2000); // Every 2 seconds
  };

  useEffect(() => {
    if (step === 4) {
      setMessages([]); // Reset messages when debate starts
      if (mode === "AI vs AI") {
        startAIDebate();
      }
    }
  }, [step]);

  return (
    <div className="flex flex-col items-center justify-start min-h-screen text-white pt-16 pb-8">
      <h1 className="text-2xl font-bold mb-4">💡Let's Begin Historical Debate...</h1>

      {step === 1 && (
        // Mode Selection
        <div className="flex flex-col items-center">
          <h2 className="text-xl mb-4">Select Debate Mode</h2>
          <div className="flex mb-4">
            <button
              className="px-4 py-2 rounded-lg bg-gray-700 text-white m-2"
              onClick={() => {
                setMode("AI vs AI");
                setStep(2);
              }}>
              AI vs AI
            </button>
            <button
              className="px-4 py-2 rounded-lg bg-gray-700 text-white m-2"
              onClick={() => {
                setMode("You vs AI");
                setStep(2);
              }}>
              You vs AI
            </button>
          </div>
        </div>
      )}

      {step === 2 && (
        // Topic Selection
        <div className="flex flex-col items-center">
          <h2 className="text-xl mb-4">Select Topic</h2>
          <div className="flex mb-4">
            <button
              className="px-4 py-2 rounded-lg bg-gray-700 text-white m-2"
              onClick={() => {
                setTopic("politics");
                setStep(3);
              }}>
              Politics
            </button>
            <button
              className="px-4 py-2 rounded-lg bg-gray-700 text-white m-2"
              onClick={() => {
                setTopic("philosophy");
                setStep(3);
              }}>
              Philosophy
            </button>
          </div>
        </div>
      )}

      {step === 3 && (
        // Figure Selection
        <div className="flex flex-col items-center">
          {mode === "AI vs AI" && (
            <div>
              <h2 className="text-xl mb-4">Select {selectedFigures.length === 0 ? "First" : "Second"} Figure</h2>
              <div className="flex mb-4">
                {["Benjamin Netanyahu", "Norman Finkelstein", "Vladimir Putin"].map((figure) => (
                  <button
                    key={figure}
                    className="px-4 py-2 rounded-lg bg-gray-700 text-white m-2"
                    onClick={() => {
                      setSelectedFigures([...selectedFigures, figure]);
                      if (selectedFigures.length === 0) {
                        // First figure selected, wait for second
                      } else {
                        // Second figure selected, proceed to next step
                        setStep(4);
                      }
                    }}>
                    {figure}
                  </button>
                ))}
              </div>
            </div>
          )}
          {mode === "You vs AI" && (
            <div>
              <h2 className="text-xl mb-4">Select a Figure to Debate</h2>
              <div className="flex mb-4">
                {["Benjamin Netanyahu", "Norman Finkelstein", "Vladimir Putin"].map((figure) => (
                  <button
                    key={figure}
                    className="px-4 py-2 rounded-lg bg-gray-700 text-white m-2"
                    onClick={() => {
                      setSelectedFigures([figure]);
                      setStep(4);
                    }}>
                    {figure}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {step === 4 && (
        // Begin Debate
        <div className="w-full max-w-2xl mb-4">
          <h2 className="text-xl mb-4">Debate Started</h2>
          {/* Chat window */}
          {messages.map((msg, index) => (
            <div key={index} className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}>
              <div
                className={`p-2 m-1 rounded-md ${
                  msg.sender === "user" ? "bg-orange-500 text-white" : "bg-gray-700 text-white"
                } max-w-full break-words`}>
                {msg.sender === "assistant" ? (
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    components={{
                      h1: ({ node, ...props }) => <h1 className="font-bold" {...props} />,
                      h2: ({ node, ...props }) => <h2 className="font-bold" {...props} />,
                      // Customize other elements if needed
                    }}>
                    {sanitizeHtml(msg.text)}
                  </ReactMarkdown>
                ) : (
                  <p>{msg.text}</p>
                )}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex justify-start mb-2">
              <div className="flex items-center p-3 rounded-lg bg-gray-700 text-white max-w-md">
                {/* Typing indicator with bouncing dots */}
                <div className="flex space-x-1 mr-2">
                  <div className="w-2 h-2 bg-white rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-white rounded-full animate-bounce delay-200"></div>
                  <div className="w-2 h-2 bg-white rounded-full animate-bounce delay-400"></div>
                </div>
                <span>Generating response...</span>
              </div>
            </div>
          )}
          {mode === "You vs AI" && (
            <>
              {/* Input area */}
              <textarea
                value={inputValue}
                onChange={handleInputChange}
                className="border border-gray-600 rounded-md p-2 mb-4 w-full max-w-2xl bg-gray-700 text-white resize-none"
                placeholder="Type your message here..."
              />
              <button className={getButtonClass("gradient")} onClick={handleSubmit}>
                <span>Send</span>
                <span className="ml-2">➔</span>
              </button>
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default IdeaGenerator;
