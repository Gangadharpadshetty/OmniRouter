# OMNICHAT Platform - Developer Quick Reference

## Start Services (4 Terminal Windows)

```powershell
# Terminal 1 - Auth Service (Port 8000)
cd F:\OMNICHAT\backend\auth_service
python main.py

# Terminal 2 - Project Service (Port 8001)
cd F:\OMNICHAT\backend\project_service
python main.py

# Terminal 3 - Chat Service (Port 8002)
cd F:\OMNICHAT\backend\chat_service
python main.py

# Terminal 4 - Frontend (Port 3000)
cd F:\OMNICHAT\frontend
npm install  # only if first time
npm start
```

## Project Endpoints

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 (local) |
| Auth Service | https://omnirouter-authservice.onrender.com |
| Project Service | https://omnirouter-project-services.onrender.com |
| Chat Service | https://omnirouter-chatservice.onrender.com |

## Frontend Routes

| Route | Purpose |
|-------|---------|
| `/` | Redirects to dashboard |
| `/login` | Login page |
| `/register` | Registration page |
| `/dashboard` | Main app (protected) |

## API Endpoints Quick List

### Auth (Port 8000)
```
POST /auth/register
  body: { email, password }
  
POST /auth/login
  body: { email, password }
  
GET /auth/verify
  headers: { Authorization: "Bearer {token}" }
```

### Projects (Port 8001)
```
GET /projects
  headers: { Authorization: "Bearer {token}" }
  
POST /projects
  body: { name, description }
  
DELETE /projects/{id}

GET /projects/{id}/prompts
POST /projects/{id}/prompts
  body: { name, content }
```

### Chat (Port 8002)
```
POST /conversations
  body: { project_id }
  
POST /conversations/{id}/messages
  body: { content }
  
GET /conversations/{id}/messages
GET /conversations/project/{id}
```

## Common Commands

### Frontend
```powershell
cd F:\OMNICHAT\frontend

# Install dependencies
npm install

# Start dev server
npm start

# Build for production
npm run build

# Run tests
npm test
```

### Backend
```powershell
# Activate virtual environment (if using venv)
venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run service
python main.py

# Run tests
pytest
```

## Check Services Running

```powershell
# Check if ports open
Test-NetConnection localhost -Port 3000
Test-NetConnection localhost -Port 8000
Test-NetConnection localhost -Port 8001
Test-NetConnection localhost -Port 8002

# Kill process on port (example: 8000)
$pid = (Get-NetTCPConnection -LocalPort 8000).OwningProcess
Stop-Process -Id $pid -Force
```

## Frontend Component Structure

```
Components/
├── AuthContext.js - Global auth state
├── Login.js - Login form
├── Register.js - Registration form
├── Dashboard.js - Main layout
├── ProfileSidebar.js - Projects sidebar
├── ChatInterface.js - Chat UI
└── api.js - API client
```

## Backend Service Structure

```
Each Service/
├── domain/ - Data models
├── repository/ - Database access
├── service/ - Business logic
├── routes/ - API endpoints
└── main.py - Entry point
```

## Testing Workflow

1. **Register Test Account**
   - Email: test@example.com
   - Password: Test123!@#

2. **Create Project**
   - Name: Test Project
   - Description: Test

3. **Create Conversation**
   - Click "Start Chat"
   - Click "New Chat"

4. **Send Message**
   - Type: "Hello"
   - Press Enter

## Browser DevTools Tips

- **Network Tab** - See API calls
- **Console Tab** - Check for errors
- **Storage > localStorage** - Check JWT token
- **React DevTools** - Inspect components

## Environment Variables

Frontend doesn't need .env (uses hardcoded localhost)

Backend uses .env for:
- DATABASE_URL
- JWT_SECRET
- OPENROUTER_API_KEY or OPENAI_API_KEY

## Database Tables

```sql
-- Check users
SELECT * FROM users LIMIT 10;

-- Check projects
SELECT * FROM projects LIMIT 10;

-- Check conversations
SELECT * FROM conversations LIMIT 10;

-- Check messages
SELECT * FROM messages LIMIT 10;
```

## Error Messages & Fixes

| Error | Fix |
|-------|-----|
| CORS error | Backend not running |
| 401 Unauthorized | Token expired, re-login |
| Port already in use | Kill process on that port |
| Module not found | Run npm install (frontend) or pip install (backend) |
| Cannot connect to DB | Check connection string in .env |
| Chat no response | Check LLM API key in .env |

## File Locations

| Item | Location |
|------|----------|
| Frontend src | F:\OMNICHAT\frontend\src\ |
| Frontend styles | F:\OMNICHAT\frontend\src\styles\ |
| Backend auth | F:\OMNICHAT\backend\auth_service\ |
| Backend project | F:\OMNICHAT\backend\project_service\ |
| Backend chat | F:\OMNICHAT\backend\chat_service\ |
| Documentation | F:\OMNICHAT\ (root) |

## Make API Call Examples

### JavaScript (Frontend)
```javascript
// In component
import { authAPI, projectAPI, chatAPI } from '../services/api';

// Register
const response = await authAPI.register(email, password);

// Create project
const response = await projectAPI.createProject(name, description);

// Send message
const response = await chatAPI.sendMessage(conversationId, message);
```

### PowerShell (Testing)
```powershell
$body = @{
  email = "test@example.com"
  password = "Test123!@#"
} | ConvertTo-Json

$response = Invoke-WebRequest -Uri "http://localhost:8000/auth/login" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body

$token = $response.Content | ConvertFrom-Json | Select -ExpandProperty access_token
echo "Token: $token"
```

## Clear Data Between Tests

```powershell
# Clear browser localStorage
# In browser console:
localStorage.clear()

# Or reset database (requires SQL access):
# In psql:
TRUNCATE messages CASCADE;
TRUNCATE conversations CASCADE;
TRUNCATE prompts CASCADE;
TRUNCATE projects CASCADE;
TRUNCATE users CASCADE;
```

## Performance Tips

1. **Frontend**
   - Check Network tab for slow requests
   - Use React DevTools Profiler
   - Clear console errors
   - Check localStorage size

2. **Backend**
   - Check database query times
   - Monitor memory usage
   - Review logs for errors
   - Test with sample data

## Debugging Checklist

- [ ] All services running on correct ports?
- [ ] Database connected?
- [ ] Token in localStorage?
- [ ] API URLs correct in frontend?
- [ ] CORS enabled in backend?
- [ ] LLM API key configured?
- [ ] Browser console clear of errors?
- [ ] Network tab shows successful requests?

## Documentation Reference

| Doc | When to Use |
|-----|-------------|
| PROJECT_SUMMARY.md | Overview of entire system |
| PLATFORM_TESTING_GUIDE.md | Full testing procedures |
| FRONTEND_SETUP_GUIDE.md | Frontend setup help |
| frontend/README.md | Frontend API details |
| frontend/QUICKSTART.md | Quick start (frontend) |
| README_PLATFORM.md | Backend overview |
| API_TEST_GUIDE.md | API testing scripts |
| QUICK_REFERENCE.md | This file |

## Useful Links

- React Docs: https://react.dev
- FastAPI Docs: http://localhost:8000/docs (when running)
- PostgreSQL: https://www.postgresql.org/docs/

## Time Estimates

| Task | Time |
|------|------|
| Install dependencies | 5 min |
| Start all services | 2 min |
| Register user | 1 min |
| Create project | 1 min |
| Test chat message | 1 min |
| Full manual test | 15 min |
| Build frontend | 2 min |

## Contact & Support

- Check documentation first
- Review console/network errors
- Check database directly
- Review service logs
- Test with curl/Postman

---

**Version:** 1.0  
**Last Updated:** Jan 16, 2026
