import React, { useState, useEffect } from 'react';
import { FiPlus, FiChevronDown, FiLogOut, FiSettings, FiTrash2, FiEdit2 } from 'react-icons/fi';
import { useAuth } from '../context/AuthContext';
import { projectAPI } from '../services/api';
import '../styles/sidebar.css';

export default function ProfileSidebar({ onSelectProject, onSelectConversation }) {
  const { user, logout } = useAuth();
  const [projects, setProjects] = useState([]);
  const [expandedProject, setExpandedProject] = useState(null);
  const [prompts, setPrompts] = useState({});
  const [loading, setLoading] = useState(true);
  const [showNewProject, setShowNewProject] = useState(false);
  const [newProjectName, setNewProjectName] = useState('');
  const [newProjectDesc, setNewProjectDesc] = useState('');

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      setLoading(true);
      const response = await projectAPI.getProjects();
      setProjects(response.data || []);
    } catch (err) {
      console.error('Failed to load projects:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadPrompts = async (projectId) => {
    if (prompts[projectId]) return;
    
    try {
      const response = await projectAPI.getPrompts(projectId);
      setPrompts(prev => ({
        ...prev,
        [projectId]: response.data || []
      }));
    } catch (err) {
      console.error('Failed to load prompts:', err);
    }
  };

  const handleCreateProject = async (e) => {
    e.preventDefault();
    if (!newProjectName.trim()) return;

    try {
      await projectAPI.createProject(newProjectName, newProjectDesc);
      setNewProjectName('');
      setNewProjectDesc('');
      setShowNewProject(false);
      loadProjects();
    } catch (err) {
      console.error('Failed to create project:', err);
    }
  };

  const handleDeleteProject = async (projectId) => {
    if (!window.confirm('Delete this project?')) return;
    
    try {
      await projectAPI.deleteProject(projectId);
      loadProjects();
    } catch (err) {
      console.error('Failed to delete project:', err);
    }
  };

  const toggleProject = async (projectId) => {
    if (expandedProject === projectId) {
      setExpandedProject(null);
    } else {
      setExpandedProject(projectId);
      await loadPrompts(projectId);
    }
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <div className="user-profile">
          <div className="avatar">
            {user?.email?.charAt(0).toUpperCase() || 'U'}
          </div>
          <div className="user-info">
            <p className="user-email">{user?.email}</p>
            <p className="user-status">Online</p>
          </div>
          <button className="menu-btn" onClick={logout} title="Logout">
            <FiLogOut />
          </button>
        </div>
      </div>

      <div className="sidebar-content">
        <div className="projects-header">
          <h3>Projects</h3>
          <button
            className="add-btn"
            onClick={() => setShowNewProject(!showNewProject)}
            title="New Project"
          >
            <FiPlus />
          </button>
        </div>

        {showNewProject && (
          <form className="new-project-form" onSubmit={handleCreateProject}>
            <input
              type="text"
              placeholder="Project name"
              value={newProjectName}
              onChange={(e) => setNewProjectName(e.target.value)}
              required
            />
            <textarea
              placeholder="Description (optional)"
              value={newProjectDesc}
              onChange={(e) => setNewProjectDesc(e.target.value)}
              rows="2"
            />
            <div className="form-actions">
              <button type="submit" className="submit-btn">Create</button>
              <button
                type="button"
                className="cancel-btn"
                onClick={() => setShowNewProject(false)}
              >
                Cancel
              </button>
            </div>
          </form>
        )}

        {loading ? (
          <div className="loading">Loading projects...</div>
        ) : projects.length === 0 ? (
          <div className="empty-state">
            <p>No projects yet</p>
            <p className="hint">Create one to get started</p>
          </div>
        ) : (
          <div className="projects-list">
            {projects.map(project => (
              <div key={project.id} className="project-item">
                <div className="project-header">
                  <button
                    className="toggle-btn"
                    onClick={() => toggleProject(project.id)}
                  >
                    <FiChevronDown
                      className={expandedProject === project.id ? 'open' : ''}
                    />
                  </button>
                  <button
                    className="project-name-btn"
                    onClick={() => onSelectProject(project)}
                  >
                    {project.name}
                  </button>
                  <button
                    className="delete-btn"
                    onClick={() => handleDeleteProject(project.id)}
                    title="Delete project"
                  >
                    <FiTrash2 />
                  </button>
                </div>

                {expandedProject === project.id && (
                  <div className="project-content">
                    <p className="project-desc">{project.description}</p>
                    
                    <div className="prompts-section">
                      <h4>Prompts</h4>
                      {!prompts[project.id] ? (
                        <p className="loading-text">Loading prompts...</p>
                      ) : prompts[project.id].length === 0 ? (
                        <p className="empty-text">No prompts yet</p>
                      ) : (
                        <div className="prompts-list">
                          {prompts[project.id].map(prompt => (
                            <div key={prompt.id} className="prompt-item">
                              <div className="prompt-name">{prompt.name}</div>
                              <div className="prompt-version">v{prompt.version}</div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>

                    <button
                      className="start-chat-btn"
                      onClick={() => onSelectProject(project)}
                    >
                      Start Chat
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="sidebar-footer">
        <button className="settings-btn">
          <FiSettings /> Settings
        </button>
      </div>
    </div>
  );
}
