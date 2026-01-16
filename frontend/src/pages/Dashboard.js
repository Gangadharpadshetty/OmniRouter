import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import ProfileSidebar from '../components/ProfileSidebar';
import ChatInterface from '../components/ChatInterface';
import '../styles/dashboard.css';

export default function Dashboard() {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [selectedProject, setSelectedProject] = useState(null);
  const [selectedConversation, setSelectedConversation] = useState(null);

  React.useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, navigate]);

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="dashboard">
      <ProfileSidebar
        onSelectProject={setSelectedProject}
        onSelectConversation={setSelectedConversation}
      />
      <ChatInterface project={selectedProject} />
    </div>
  );
}
