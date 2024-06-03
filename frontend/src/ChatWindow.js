import { React, useState, useEffect, useContext } from "react";
import "./ChatWindow.css";
import MapContext from "./MapContext";

const SERVER_URL = process.env.REACT_APP_BACKEND_URL;

function ChatWindow({ handleClose, isActive }) {
  const { userLocation } = useContext(MapContext);
  const [messages, setMessages] = useState([
    {
      id: 0,
      sender: "chatbot",
      text: "Hello! What can I help you today?",
      timestamp: new Date(),
    },
  ]);
  const [newMessage, setNewMessage] = useState("");
  const [sessionID, setSessionID] = useState("");
  const [conversationID, setConversationID] = useState("");

  const startConversation = async (session_id) => {
    const response = await fetch(`${SERVER_URL}/chatbot/conversation/start`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id }),
    });
    const data = await response.json();
    setConversationID(data.conversation_id);
  };

  useEffect(() => {
    const startSession = async () => {
      const response = await fetch(`${SERVER_URL}/chatbot/session/start`, {
        method: "POST",
      });
      const data = await response.json();
      setSessionID(data.session_id);
      startConversation(data.session_id);
    };
    startSession();
  }, []);

  // Function for sending a new message
  const sendMessage = async (event) => {
    event.preventDefault(); // Prevent the reload of the page
    if (newMessage !== "") {
      const newMessageObj = {
        id: messages.length,
        sender: "user",
        text: newMessage,
        timestamp: new Date(),
      };
      setMessages([...messages, newMessageObj]);
      setNewMessage(""); // Clear input box

      /* The part for sending the message list to the backend */
      try {
        const response = await fetch(`${SERVER_URL}/chatbot/message/send`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            session_id: sessionID,
            conversation_id: conversationID,
            text: newMessageObj.text,
            context:
              messages.length >= 3
                ? `user: ${messages[messages.length - 3].text} ` +
                  `ai: ${messages[messages.length - 2].text}`
                : "",
            lat: userLocation.lat,
            lng: userLocation.lng,
          }),
        });

        let response_json = await response.json();
        setMessages((prevMessages) => [
          ...prevMessages,
          {
            id: prevMessages.length,
            sender: "chatbot",
            text: response_json.ai_response.text,
            timestamp: new Date(),
          },
        ]);
      } catch (error) {
        console.error("Failed to send message:", error);
      }
    }
  };

  const handleCloseWindow = () => {
    handleClose();
    /*
    setMessages([
      {
        id: 0,
        sender: "chatbot",
        text: "Hello! What can I help you today?",
        timestamp: new Date(),
      },
    ]); // Clear all the messages
    */
  };

  return (
    <div className={isActive ? "chat-window" : "chat-window active"}>
      <div className="chat-header">Chat Support</div>
      <div className="chat-content">
        {messages.map((message) => {
          return (
            <div
              key={message.id}
              className={`message ${
                message.sender === "user" ? "user-message" : "chatbot-message"
              }`}
            >
              {message.text}
            </div>
          );
        })}
      </div>
      <div className="chat-input-container">
        <form className="chat-input-bar" onSubmit={sendMessage}>
          <input
            type="text"
            className="chat-input"
            placeholder="Type a message..."
            value={newMessage}
            onChange={(event) => {
              setNewMessage(event.target.value);
            }}
          />
          <button type="submit" className="send-button">
            <svg
              class="send-icon"
              fill="currentColor"
              viewBox="0 0 24 24"
              width="24"
              height="24"
            >
              <path d="M2,21L23,12L2,3V10L17,12L2,14V21Z" />
            </svg>
          </button>
        </form>
      </div>
      <button
        className="close-button"
        onClick={handleCloseWindow}
        title="Close"
      >
        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <line x1="18" y1="6" x2="6" y2="18"></line>
          <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
      </button>
    </div>
  );
}

export default ChatWindow;
