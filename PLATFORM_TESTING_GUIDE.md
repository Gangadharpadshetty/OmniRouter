# OMNICHAT Platform - Complete Testing & Deployment Guide

## System Overview

OMNICHAT is a microservices-based AI chatbot platform consisting of:

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend (React)                      │
│              http://localhost:3000                      │
└─────────────────────────────────────────────────────────┘
         ↓                    ↓                    ↓
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  Auth Service    │  │ Project Service  │  │  Chat Service    │
│ :8000 (FastAPI)  │  │ :8001 (FastAPI)  │  │ :8002 (FastAPI)  │
└──────────────────┘  └──────────────────┘  └──────────────────┘
         ↓                    ↓                    ↓
┌─────────────────────────────────────────────────────────┐
│        PostgreSQL Database (External)                   │
└─────────────────────────────────────────────────────────┘
```

## Pre-Testing Checklist

- [ ] PostgreSQL is running and accessible
- [ ] Database `omnichat` exists
- [ ] Python 3.10+ installed
- [ ] Node.js 14+ and npm installed
- [ ] Virtual environment activated (backend)
- [ ] All dependencies installed
- [ ] `.env` files configured with API keys

## Step 1: Backend Services (Render Deployment)

Backend services are deployed on Render and running at:

- **Auth Service**: https://omnirouter-authservice.onrender.com
- **Project Service**: https://omnirouter-project-services.onrender.com
- **Chat Service**: https://omnirouter-chatservice.onrender.com

### Verify Services Running

Test connectivity to each service:

```powershell
# Test Auth Service
Test-NetConnection omnirouter-authservice.onrender.com -Port 443

# Test Project Service
Test-NetConnection omnirouter-project-services.onrender.com -Port 443

# Test Chat Service
Test-NetConnection omnirouter-chatservice.onrender.com -Port 443
```

Or use PowerShell to test endpoints:
```powershell
# Test Auth Service
Invoke-WebRequest -Uri "https://omnirouter-authservice.onrender.com/auth/verify" -Method GET

# Test Project Service
Invoke-WebRequest -Uri "https://omnirouter-project-services.onrender.com/projects" -Method GET

# Test Chat Service
Invoke-WebRequest -Uri "https://omnirouter-chatservice.onrender.com/conversations" -Method GET
```

## Step 2: Test Backend APIs

### 2.1 Run API Test Script

```powershell
cd F:\OMNICHAT
.\test-api.ps1
```

This tests:
- Auth registration
- User login
- Project CRUD
- Prompt management
- Conversation creation
- Message sending

### 2.2 Check Database

Connect to PostgreSQL:
```powershell
psql -U your_user -d omnichat
```

Verify tables:
```sql
\dt
-- Should show: users, projects, prompts, conversations, messages
```

## Step 3: Start Frontend

### 3.1 Install Dependencies

```powershell
cd F:\OMNICHAT\frontend
npm install
```

### 3.2 Start Development Server

```powershell
npm start
```

Expected output:
```
Compiled successfully!

You can now view omnichat-frontend in the browser.

  http://localhost:3000

Note that the development build is not optimized.
```

Browser will open automatically at `http://localhost:3000`

## Step 4: Manual Testing

### Test 1: User Registration

1. Click "Register" link
2. Enter:
   - Email: `test@example.com`
   - Password: `Test123!@#`
   - Confirm: `Test123!@#`
3. Click "Register"
4. Should see dashboard automatically

**Expected Results:**
- User account created in database
- JWT token stored in localStorage
- Redirected to dashboard
- User email visible in sidebar

### Test 2: Project Management

1. In sidebar, click "+" button
2. Enter:
   - Name: `AI Assistant v1`
   - Description: `My first AI project`
3. Click "Create"

**Expected Results:**
- Project appears in sidebar
- Can expand to see details
- Delete button functional
- Project appears in database

### Test 3: Prompt Management

After creating project:

1. Prompts should display under project (if any exist)
2. Version numbers show correctly
3. System prompt information visible

**Expected Results:**
- Prompts displayed with versions
- Can see all project prompts
- Correct formatting

### Test 4: Chat Functionality

1. Click "Start Chat" on project
2. Click "New Chat" button
3. Type: `Hello, can you help me?`
4. Press Enter or click Send

**Expected Results:**
- User message appears on right (blue)
- Message appears in message list
- Loading indicator shows
- AI response appears on left (gray)
- Conversation appears in left sidebar

### Test 5: Conversation History

1. Send multiple messages
2. Click different conversation in left sidebar
3. Click back to previous conversation

**Expected Results:**
- Messages load correctly
- Conversation history preserved
- Can switch between conversations
- All messages display correctly

### Test 6: Logout & Login

1. Click user avatar dropdown (or logout button when added)
2. Click "Logout"
3. Should redirect to login page
4. Login with same credentials

**Expected Results:**
- Token cleared from localStorage
- Redirected to login
- Can login successfully
- All data preserved in database

## Step 5: API Integration Testing

### Test Direct API Calls

```powershell
# Test Auth Service
$headers = @{
  "Content-Type" = "application/json"
}
$body = @{
  email = "test@example.com"
  password = "Test123!@#"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/auth/login" `
  -Method POST `
  -Headers $headers `
  -Body $body
```

Expected response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

## Step 6: Performance Testing

### Test Load

1. Create multiple projects (5-10)
2. Create multiple conversations (10-20 per project)
3. Send multiple messages (20+ per conversation)

**Verify:**
- No performance degradation
- Sidebar loads quickly
- Messages display smoothly
- No memory leaks

## Step 7: Error Handling

### Test Error Scenarios

1. **Invalid credentials**
   - Try login with wrong password
   - Should see error message

2. **Duplicate email**
   - Try registering with existing email
   - Should see error message

3. **Offline backend**
   - Stop one backend service
   - Try using that feature
   - Should show connection error

4. **Invalid input**
   - Try creating project with empty name
   - Form should prevent submission

## Production Deployment

### Frontend Build

```powershell
cd F:\OMNICHAT\frontend
npm run build
```

Deploy `build/` directory to:
- Vercel
- Netlify
- AWS S3 + CloudFront
- Traditional web server (nginx, Apache)

### Backend Deployment

1. Use production ASGI server (Gunicorn, Uvicorn)
2. Configure environment variables
3. Set up database backups
4. Enable CORS for frontend domain
5. Use HTTPS/TLS
6. Set up logging and monitoring

Example with Gunicorn:
```powershell
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
```

### Database

1. Use managed PostgreSQL (AWS RDS, Azure Database)
2. Configure backups
3. Set up replication
4. Enable SSL connections
5. Restrict network access

## Monitoring

### Key Metrics to Monitor

- Response times (target < 200ms)
- Error rates (target < 0.1%)
- Database query times
- Memory usage
- API token expiration issues

### Logging

Enable logging in:
- `backend/auth_service/main.py`
- `backend/project_service/main.py`
- `backend/chat_service/main.py`

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| CORS errors | Backend not running | Start all 3 services |
| 401 errors | Invalid token | Clear localStorage, re-login |
| Chat not responding | Chat service down | Verify port 8002 |
| Projects not loading | Project service down | Verify port 8001 |
| Database errors | DB not accessible | Check connection string |

### Debug Commands

```powershell
# Check processes
Get-Process | Select-String python

# Kill process on port
Stop-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess -Force

# Check logs
Get-Content *.log -Tail 50

# Test connectivity
Test-NetConnection localhost -Port 8000
```

## Rollback Procedure

If issues occur in production:

1. Stop frontend deployment
2. Revert to previous backend version (keep DB)
3. Clear browser cache
4. Notify users
5. Investigate logs
6. Fix and test thoroughly before re-deploy

## Maintenance

### Daily
- Monitor error logs
- Check system health
- Verify backups

### Weekly
- Review performance metrics
- Check database size
- Update dependencies (dev only)

### Monthly
- Full backup verification
- Security audit
- Performance analysis

## Support

For issues:
1. Check logs first
2. Review API documentation
3. Test with sample data
4. Check browser DevTools Network tab
5. Verify backend connectivity

## Documentation

- API_TEST_GUIDE.md - Automated API testing
- README_PLATFORM.md - Backend setup
- FRONTEND_SETUP_GUIDE.md - Frontend setup
- This guide - Complete testing procedures
