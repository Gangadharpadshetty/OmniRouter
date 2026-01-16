# OMNICHAT Quick Start Guide

## Prerequisites

- Python 3.13+
- PostgreSQL (external database already configured)
- PowerShell

## Step 1: Install Dependencies for All Services

```powershell
cd F:\OMNICHAT\auth-service
pip install -r requirements.txt

cd F:\OMNICHAT\project-service
pip install -r requirements.txt

cd F:\OMNICHAT\chat-service
pip install -r requirements.txt
```

## Step 2: Start Services (Open 3 separate terminal windows)

### Terminal 1 - Auth Service (Port 8000)
```powershell
cd F:\OMNICHAT\auth-service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2 - Project Service (Port 8001)
```powershell
cd F:\OMNICHAT\project-service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8001
```

### Terminal 3 - Chat Service (Port 8002)
```powershell
cd F:\OMNICHAT\chat-service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8002
```

## Step 3: Run the Test Script

Once all three services are running, open a new terminal and run:

```powershell
cd F:\OMNICHAT
.\test-api-local.ps1
```

## Expected Output

The script will:

1. ✅ Register a new user with a random email
2. ✅ Login and get JWT token
3. ✅ Create a project named "AI Customer Service Bot"
4. ✅ Create a prompt for the project
5. ✅ List all projects
6. ✅ Get project details
7. ✅ List all prompts
8. ✅ Create a conversation
9. ⚠️ Send a message (will fail if LLM API is not configured)
10. ✅ Get conversation history
11. ✅ List project conversations

## Accessing the Services

Once running, you can access:

- **Auth Service Docs:** http://localhost:8000/docs
- **Project Service Docs:** http://localhost:8001/docs
- **Chat Service Docs:** http://localhost:8002/docs

## Troubleshooting

### ModuleNotFoundError: No module named 'app'
**Solution:** Make sure you run uvicorn from the service root directory, not from the `app/` or `scripts/` subdirectory.

### 401 Unauthorized
**Solution:** JWT tokens from one service won't work with another if they have different JWT_SECRET values. Make sure all services use the same JWT_SECRET from their `.env` files.

### 404 Not Found
**Solution:** Make sure the service is running on the correct port. Check that all three terminals show "Uvicorn running on..."

### Database Connection Error
**Solution:** Check that:
1. The DATABASE_URL in `.env` files is correct
2. The PostgreSQL server is accessible
3. All required tables exist

## Database Setup

The database tables should be automatically created when using SQLAlchemy ORM. If they don't exist, run these SQL commands:

```sql
-- Users table (auth-service)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Projects table (project-service)
CREATE TABLE IF NOT EXISTS projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    description VARCHAR(1000),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Prompts table (project-service)
CREATE TABLE IF NOT EXISTS prompts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    content VARCHAR(10000) NOT NULL,
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Conversations table (chat-service)
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Messages table (chat-service)
CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL,
    content VARCHAR(10000) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Next Steps

- View API documentation at service `/docs` endpoints (Swagger UI)
- Check `API_TEST_GUIDE.md` for detailed API endpoint documentation
- Review `ARCHITECTURE.md` for system design details
- Check individual service READMEs for service-specific information

## Manual Testing with curl

### Register a user:
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

### Login:
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'
```

### Create a project (replace TOKEN with JWT from login):
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X POST http://localhost:8001/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"My Bot","description":"Test bot"}'
```

## Deployment

When ready to deploy:

1. Update `.env` files with production settings
2. Set `DEBUG=False` in environment
3. Deploy using Docker or your preferred platform
4. See deployment section in `ARCHITECTURE.md`
