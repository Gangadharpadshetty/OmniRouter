import React, { useState, useEffect, useRef } from 'react';
import { FiSend, FiPlus, FiX } from 'react-icons/fi';
import { chatAPI } from '../services/api';
import '../styles/chat.css';

export default function ChatInterface({ project }) {
  const [conversations, setConversations] = useState([]);
  const [activeConversation, setActiveConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationLoading, setConversationLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (project) {
      loadConversations();
    }
  }, [project]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const loadConversations = async () => {
    try {
      setConversationLoading(true);
      setError(null);
      const response = await chatAPI.listProjectConversations(project.id);
      setConversations(response.data || []);
      if (response.data && response.data.length > 0) {
        selectConversation(response.data[0]);
      }
    } catch (err) {
      console.error('Failed to load conversations:', err);
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to load conversations';
      setError(errorMsg);
    } finally {
      setConversationLoading(false);
    }
  };

  const createNewConversation = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await chatAPI.createConversation(project.id);
      const newConversation = response.data;
      setConversations(prev => [newConversation, ...prev]);
      selectConversation(newConversation);
    } catch (err) {
      console.error('Failed to create conversation:', err);
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to create conversation';
      setError(errorMsg);
      alert(`Error: ${errorMsg}`);
    } finally {
      setLoading(false);
    }
  };

  const selectConversation = async (conversation) => {
    setActiveConversation(conversation);
    setMessages([]);
    setError(null);
    try {
      const response = await chatAPI.getConversationMessages(conversation.id);
      setMessages(response.data || []);
    } catch (err) {
      console.error('Failed to load messages:', err);
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to load messages';
      setError(errorMsg);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || !activeConversation) return;

    const userMessage = inputValue;
    const tempId = 'temp-' + Date.now();
    setInputValue('');
    setLoading(true);
    setError(null);

    try {
      // Add user message to UI optimistically
      setMessages(prev => [...prev, {
        id: tempId,
        role: 'user',
        content: userMessage,
        created_at: new Date().toISOString()
      }]);

      // Send message to backend
      const response = await chatAPI.sendMessage(activeConversation.id, userMessage);
      
      // Add assistant response
      if (response.data && response.data.response) {
        setMessages(prev => [...prev, {
          id: 'assistant-' + Date.now(),
          role: 'assistant',
          content: response.data.response,
          created_at: new Date().toISOString()
        }]);
      }
    } catch (err) {
      console.error('Failed to send message:', err);
      const errorMsg = err.response?.data?.detail || err.message || 'Failed to send message';
      setError(errorMsg);
      // Remove optimistic user message on error
      setMessages(prev => prev.filter(msg => msg.id !== tempId));
      alert(`Error: ${errorMsg}`);
    } finally {
      setLoading(false);
    }
  };

  if (!project) {
    return (
      <div className="chat-container empty">
        <div className="empty-state">
          <h2>Select a project to start chatting</h2>
          <p>Choose a project from the sidebar to begin</p>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="project-info">
          <h2>{project.name}</h2>
          <p>{project.description}</p>
        </div>
        <button
          className="new-conversation-btn"
          onClick={createNewConversation}
          disabled={loading}
          title="New Conversation"
        >
          <FiPlus /> New Chat
        </button>
      </div>

      <div className="chat-content">
        {error && (
          <div className="error-banner" style={{ 
            padding: '10px', 
            margin: '10px', 
            background: '#fee', 
            color: '#c00',
            borderRadius: '4px',
            fontSize: '14px'
          }}>
            {error}
          </div>
        )}

        <div className="conversations-panel">
          <h3>Conversations</h3>
          {conversationLoading ? (
            <div className="loading">Loading conversations...</div>
          ) : conversations.length === 0 ? (
            <div className="empty-text">
              <p>No conversations yet</p>
              <button
                className="create-btn"
                onClick={createNewConversation}
                disabled={loading}
              >
                Start First Chat
              </button>
            </div>
          ) : (
            <div className="conversations-list">
              {conversations.map(conv => (
                <button
                  key={conv.id}
                  className={`conversation-item ${activeConversation?.id === conv.id ? 'active' : ''}`}
                  onClick={() => selectConversation(conv)}
                >
                  <span className="conv-title">Chat {conversations.indexOf(conv) + 1}</span>
                  <span className="conv-date">
                    {new Date(conv.created_at).toLocaleDateString()}
                  </span>
                </button>
              ))}
            </div>
          )}
        </div>

        <div className="messages-panel">
          {!activeConversation ? (
            <div className="empty-state">
              <h3>No conversation selected</h3>
              <button
                className="primary-btn"
                onClick={createNewConversation}
                disabled={loading}
              >
                Start New Conversation
              </button>
            </div>
          ) : (
            <>
              <div className="messages-list">
                {messages.length === 0 ? (
                  <div className="empty-state">
                    <p>Start the conversation by sending a message</p>
                  </div>
                ) : (
                  messages.map(msg => (
                    <div
                      key={msg.id}
                      className={`message ${msg.role === 'user' ? 'user-message' : 'assistant-message'}`}
                    >
                      <div className="message-content">
                        <p>{msg.content}</p>
                        <span className="message-time">
                          {new Date(msg.created_at).toLocaleTimeString()}
                        </span>
                      </div>
                    </div>
                  ))
                )}
                <div ref={messagesEndRef} />
              </div>

              <form className="message-input-form" onSubmit={handleSendMessage}>
                <input
                  type="text"
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  placeholder="Type your message..."
                  disabled={loading}
                  autoFocus
                />
                <button
                  type="submit"
                  disabled={loading || !inputValue.trim()}
                  className="send-btn"
                  title="Send message"
                >
                  <FiSend />
                </button>
              </form>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
