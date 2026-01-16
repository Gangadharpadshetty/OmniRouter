# OMNICHAT Frontend

A modern React-based web interface for the OMNICHAT AI Chatbot Platform.

## Features

- **User Authentication** - Register and login with JWT tokens
- **Project Management** - Create, view, and manage AI projects/agents
- **Prompt Management** - Store and manage system prompts for each project
- **Chat Interface** - Interactive chat with AI assistants
- **Conversation History** - View and manage conversation threads
- **Profile Sidebar** - Quick access to all projects and conversations
- **Real-time Updates** - Live chat responses and message updates

## Prerequisites

- Node.js 14+
- npm or yarn
- React 18+

## Installation

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Configure API endpoints** in `src/services/api.js`:
```javascript
const API_BASE_URLs = {
  auth: 'http://localhost:8000',    // Auth Service
  project: 'http://localhost:8001',  // Project Service
  chat: 'http://localhost:8002'      // Chat Service
};
```

3. **Start the development server:**
```bash
npm start
```

The application will open at `http://localhost:3000`

## Project Structure

```
frontend/
├── public/
├── src/
│   ├── components/
│   │   ├── ProfileSidebar.js      # User profile & projects sidebar
│   │   └── ChatInterface.js         # Main chat interface
│   ├── context/
│   │   └── AuthContext.js          # Global authentication state
│   ├── pages/
│   │   ├── Login.js                # Login page
│   │   ├── Register.js             # Registration page
│   │   └── Dashboard.js            # Main dashboard
│   ├── services/
│   │   └── api.js                  # Backend API client
│   ├── styles/
│   │   ├── global.css              # Global styles
│   │   ├── auth.css                # Auth pages styles
│   │   ├── dashboard.css           # Dashboard layout
│   │   ├── sidebar.css             # Sidebar component styles
│   │   └── chat.css                # Chat interface styles
│   ├── App.js                      # Main app component
│   ├── index.js                    # React entry point
│   └── index.css                   # Root styles
└── package.json
```

## Usage

### Authentication

1. **Register** - Create a new account with email and password
2. **Login** - Sign in with your credentials
3. **Dashboard** - Access your projects and conversations

### Projects

- **Create Project** - Click the "+" button in the sidebar
- **View Details** - Expand a project to see its prompts
- **Start Chat** - Click "Start Chat" button to begin conversation
- **Delete Project** - Click the trash icon to remove a project

### Chat

- **New Conversation** - Click "New Chat" button in the header
- **Send Message** - Type message and click send or press Enter
- **View History** - Click conversation to view message history
- **Switch Conversations** - Select different conversations from the sidebar

## API Integration

The frontend communicates with three microservices:

### Auth Service (Port 8000)
- `POST /auth/register` - Register new user
- `POST /auth/login` - Authenticate user

### Project Service (Port 8001)
- `GET /projects` - List user's projects
- `POST /projects` - Create new project
- `GET /projects/{id}` - Get project details
- `PUT /projects/{id}` - Update project
- `DELETE /projects/{id}` - Delete project
- `GET /projects/{id}/prompts` - List project prompts
- `POST /projects/{id}/prompts` - Create prompt
- `PUT /projects/{id}/prompts/{id}` - Update prompt
- `DELETE /projects/{id}/prompts/{id}` - Delete prompt

### Chat Service (Port 8002)
- `POST /conversations` - Create conversation
- `GET /conversations/{id}` - Get conversation
- `GET /conversations/{id}/messages` - Get messages
- `POST /conversations/{id}/messages` - Send message
- `GET /conversations/project/{id}` - List conversations
- `DELETE /conversations/{id}` - Delete conversation

## Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` directory.

## Environment Setup

Create a `.env` file if needed:
```
REACT_APP_API_AUTH_URL=http://localhost:8000
REACT_APP_API_PROJECT_URL=http://localhost:8001
REACT_APP_API_CHAT_URL=http://localhost:8002
```

## Troubleshooting

### CORS Issues
If you encounter CORS errors, ensure:
1. Backend services are running
2. API URLs in `src/services/api.js` are correct
3. Backend CORS headers are properly configured

### Token Expiration
Tokens are stored in localStorage and automatically included in requests. Clear localStorage if you encounter auth issues:
```javascript
localStorage.clear()
```

### Connection Errors
Ensure all three backend services are running on their configured ports (8000, 8001, 8002)

## Technologies Used

- **React 18** - UI framework
- **React Router** - Navigation
- **Axios** - HTTP client
- **React Icons** - Icon components
- **CSS3** - Styling

## License

Proprietary - OMNICHAT Platform

## Support

For issues or questions, refer to the main OMNICHAT documentation.
