# Frontend Quick Start

## Setup Instructions

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start the development server:**
```bash
npm start
```

The application will automatically open at `http://localhost:3000`.

## Prerequisites

- Ensure backend services are running on the expected ports:
  - Auth Service: `http://localhost:8000`
  - Project Service: `http://localhost:8001`
  - Chat Service: `http://localhost:8002`

- Recommended to run the backend test script first to verify all services are operational

## First Time Setup

1. **Create an account:**
   - Click "Register" link on the login page
   - Enter email and password
   - Click "Register"

2. **Create a project:**
   - Click the "+" button in the Projects section
   - Enter project name and description
   - Click "Create"

3. **Start chatting:**
   - Click the "Start Chat" button for your project
   - Click "New Chat" to create a conversation
   - Type a message and press enter

## Available Routes

- `/login` - Login page
- `/register` - Registration page  
- `/dashboard` - Main dashboard (protected)
- `/` - Redirects to dashboard

## Troubleshooting

**Module not found errors:** Run `npm install` again

**CORS errors:** Verify backend services are running on correct ports

**Login not working:** Check backend auth service is running

**Chat not responding:** Verify chat service and project service are running

## Build for Production

```bash
npm run build
```

Output will be in the `build/` directory.
