# OMNICHAT Frontend Setup & Integration Guide

## Overview

The OMNICHAT frontend is a React-based web application that communicates with three backend microservices:
- **Auth Service** (Port 8000)
- **Project Service** (Port 8001)
- **Chat Service** (Port 8002)

## Prerequisites

Before starting the frontend, ensure:

1. **Node.js & npm installed** (v14+)
   ```powershell
   node --version
   npm --version
   ```

2. **Backend services deployed** on Render
   - Auth Service: https://omnirouter-authservice.onrender.com
   - Project Service: https://omnirouter-project-services.onrender.com
   - Chat Service: https://omnirouter-chatservice.onrender.com

3. **Internet connection** (to access Render services)

## Installation Steps

### 1. Navigate to Frontend Directory
```powershell
cd F:\OMNICHAT\frontend
```

### 2. Install Dependencies
```powershell
npm install
```

This will install:
- React 18.2.0
- React Router 6.20.0
- Axios 1.6.0
- React Icons 4.12.0
- Tailwind CSS 3.3.0

### 3. Start Development Server
```powershell
npm start
```

The app will open automatically at `http://localhost:3000`

## API Configuration

The frontend is configured to connect to the Render deployment services:
- **Auth Service**: `https://omnirouter-authservice.onrender.com`
- **Project Service**: `https://omnirouter-project-services.onrender.com`
- **Chat Service**: `https://omnirouter-chatservice.onrender.com`

To change these URLs, edit `src/services/api.js`:
```javascript
const API_BASE_URLs = {
  auth: 'https://omnirouter-authservice.onrender.com',
  project: 'https://omnirouter-project-services.onrender.com',
  chat: 'https://omnirouter-chatservice.onrender.com'
};
```

## Directory Structure

```
frontend/
├── public/
│   └── index.html              # HTML template
├── src/
│   ├── components/
│   │   ├── ChatInterface.js    # Chat UI component
│   │   └── ProfileSidebar.js   # Sidebar with projects
│   ├── context/
│   │   └── AuthContext.js      # Authentication context
│   ├── pages/
│   │   ├── Login.js            # Login page
│   │   ├── Register.js         # Registration page
│   │   └── Dashboard.js        # Main dashboard
│   ├── services/
│   │   └── api.js              # API client
│   ├── styles/
│   │   ├── global.css          # Global styles
│   │   ├── auth.css            # Auth pages styles
│   │   ├── sidebar.css         # Sidebar styles
│   │   ├── chat.css            # Chat styles
│   │   └── dashboard.css       # Dashboard styles
│   ├── App.js                  # Main app component
│   └── index.js                # Entry point
├── package.json
├── README.md
└── QUICKSTART.md
```

## User Flow

### 1. Authentication
- User lands on `/login`
- Can register new account on `/register`
- After login/register, redirected to `/dashboard`
- JWT token stored in localStorage

### 2. Dashboard
- Left sidebar shows user profile and projects
- Click "+" to create new project
- Expand projects to see prompts
- Main area shows chat interface

### 3. Chat
- Select project from sidebar
- Click "New Chat" to create conversation
- Type message and press Enter or click Send
- View conversation history in left panel

## Testing Workflow

### Test Registration & Login
1. Open frontend at `http://localhost:3000`
2. Click "Register"
3. Enter email and password
4. Click "Register" - should auto-login
5. Should see dashboard with empty projects

### Test Project Creation
1. In sidebar, click "+" button
2. Enter project name: "Test Project"
3. Add optional description
4. Click "Create"
5. Project should appear in sidebar

### Test Chat
1. Click "Start Chat" on a project
2. Click "New Chat" button
3. Type test message
4. Press Enter or click Send button
5. Should see message appear as user message
6. AI response should appear as assistant message

## Common Issues & Solutions

### Issue: "Cannot GET /login"
**Solution:** Frontend server not running. Run `npm start`

### Issue: CORS errors in console
**Solution:** 
- Backend services not running
- Wrong port configured in `src/services/api.js`
- Backend needs CORS headers

### Issue: 401 Unauthorized
**Solution:**
- Token expired - logout and login again
- Backend auth service not running
- Clear localStorage: `localStorage.clear()`

### Issue: Projects not loading
**Solution:**
- Project service not running on port 8001
- Check database connection in backend
- Verify user is authenticated

### Issue: Chat not responding
**Solution:**
- Chat service not running on port 8002
- Check LLM API credentials (OpenRouter/OpenAI)
- Verify conversation created successfully

## Building for Production

```powershell
npm run build
```

Creates optimized production build in `build/` directory. 

To serve:
```powershell
npm install -g serve
serve -s build
```

## Environment Variables (Optional)

Create `.env` file in frontend directory:
```
REACT_APP_API_AUTH_URL=http://localhost:8000
REACT_APP_API_PROJECT_URL=http://localhost:8001
REACT_APP_API_CHAT_URL=http://localhost:8002
```

## Performance Notes

- Messages are paginated (not implemented in current version)
- Consider adding:
  - Message virtualization for large conversations
  - Conversation pagination
  - Optimistic UI updates (already implemented)
  - Caching layer

## Browser Support

Tested on:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Next Steps

1. **Start all backend services** (see README_PLATFORM.md in backend)
2. **Run frontend**: `npm start` in frontend directory
3. **Test user flow** (register → create project → chat)
4. **Check browser console** for any errors
5. **Review API calls** in Network tab of DevTools

## Development Tips

- Use React DevTools extension for debugging components
- Check Network tab to verify API calls
- Use Console for error messages
- Clear localStorage if auth issues: `localStorage.clear()`
- Hot reload enabled - save file to see changes immediately

## Documentation

- Frontend README: `frontend/README.md`
- Quick Start: `frontend/QUICKSTART.md`
- Backend Setup: `README_PLATFORM.md`
- API Testing: `API_TEST_GUIDE.md`
