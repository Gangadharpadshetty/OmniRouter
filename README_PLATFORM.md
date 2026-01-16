# OMNICHAT - AI-Powered Chatbot Platform

A scalable microservices-based platform for creating and managing AI chatbots with support for multiple LLM providers.

## Overview

OMNICHAT consists of three microservices that work together to provide a complete chatbot platform:

1. **Auth Service** - User authentication and JWT token management
2. **Project Service** - Project/agent management and prompt storage
3. **Chat Service** - Chat interactions with LLM providers

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Client Application                     │
└──────────────┬──────────────┬──────────────┬────────────────┘
               │              │              │
        ┌──────▼────┐  ┌──────▼────┐  ┌──────▼────┐
        │Auth       │  │Project    │  │Chat      │
        │Service    │  │Service    │  │Service   │
        │:8000      │  │:8001      │  │:8002     │
        └───┬───────┘  └───┬───────┘  └───┬──────┘
            │              │              │
            └──────────────┬──────────────┘
                           │
                   ┌───────▼────────┐
                   │  PostgreSQL    │
                   │  (External DB) │
                   └────────────────┘
```

## Services

### Auth Service (Port 8000)
Handles user authentication and token generation.

**Key Features:**
- User registration with email and password
- Login with JWT token generation
- Password hashing with bcrypt

**Database Tables:**
- `users` - User accounts

**Endpoints:**
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user and get token

### Project Service (Port 8001)
Manages projects/agents and their associated prompts.

**Key Features:**
- Create and manage projects under users
- Store and version prompts
- User-based access control

**Database Tables:**
- `projects` - User projects/agents
- `prompts` - Project prompts (versioned)

**Endpoints:**
- `POST /projects` - Create project
- `GET /projects` - List user projects
- `GET /projects/{id}` - Get project details
- `PUT /projects/{id}` - Update project
- `DELETE /projects/{id}` - Delete project
- `POST /projects/{id}/prompts` - Create prompt
- `GET /projects/{id}/prompts` - List prompts
- `PUT /projects/{id}/prompts/{prompt_id}` - Update prompt
- `DELETE /projects/{id}/prompts/{prompt_id}` - Delete prompt

### Chat Service (Port 8002)
Handles conversations and LLM interactions.

**Key Features:**
- Create conversations per project
- Send messages and receive LLM responses
- Maintain conversation history
- Support for OpenRouter and OpenAI

**Database Tables:**
- `conversations` - Chat conversations
- `messages` - Chat messages

**Endpoints:**
- `POST /conversations?project_id={id}` - Create conversation
- `GET /conversations/{id}` - Get conversation
- `GET /conversations/{id}/messages` - Get conversation history
- `POST /conversations/{id}/messages` - Send message
- `GET /conversations/project/{project_id}` - List project conversations
- `DELETE /conversations/{id}` - Delete conversation

## Getting Started

### Prerequisites

- Python 3.13+
- PostgreSQL (external or local)
- OpenRouter or OpenAI API key

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd OMNICHAT
   ```

2. **Set up Auth Service**
   ```bash
   cd auth-service
   pip install -r requirements.txt
   # Configure .env with DATABASE_URL and JWT_SECRET
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

3. **Set up Project Service**
   ```bash
   cd project-service
   pip install -r requirements.txt
   # Configure .env with DATABASE_URL and JWT_SECRET
   uvicorn app.main:app --host 0.0.0.0 --port 8001
   ```

4. **Set up Chat Service**
   ```bash
   cd chat-service
   pip install -r requirements.txt
   # Configure .env with DATABASE_URL, JWT_SECRET, LLM_PROVIDER, and API keys
   uvicorn app.main:app --host 0.0.0.0 --port 8002
   ```

### Database Setup

Create the required tables using SQL:

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

## API Usage Example

### 1. Register User
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secure_password"}'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secure_password"}'
# Returns: {"access_token": "token", "token_type": "bearer"}
```

### 3. Create Project
```bash
TOKEN="your-token-here"
curl -X POST http://localhost:8001/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Bot", "description": "My first chatbot"}'
```

### 4. Create Prompt
```bash
PROJECT_ID="project-uuid"
curl -X POST http://localhost:8001/projects/$PROJECT_ID/prompts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "System Prompt", "content": "You are a helpful assistant."}'
```

### 5. Create Conversation
```bash
curl -X POST "http://localhost:8002/conversations?project_id=$PROJECT_ID" \
  -H "Authorization: Bearer $TOKEN"
# Returns: {"id": "conversation-uuid", ...}
```

### 6. Send Message
```bash
CONVERSATION_ID="conversation-uuid"
curl -X POST http://localhost:8002/conversations/$CONVERSATION_ID/messages \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello, how are you?"}'
```

## Configuration

### Environment Variables

**Common to all services:**
- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET` - Secret key for JWT tokens
- `JWT_ALGORITHM` - JWT algorithm (default: HS256)

**Chat Service specific:**
- `LLM_PROVIDER` - `openrouter` or `openai` (default: openrouter)
- `LLM_MODEL` - Model identifier (default: openai/gpt-3.5-turbo)
- `OPENROUTER_API_KEY` - OpenRouter API key
- `OPENAI_API_KEY` - OpenAI API key

## Security Considerations

1. **JWT Tokens** - All services validate JWT tokens using the same secret key
2. **User Isolation** - Users can only access their own projects and conversations
3. **Database** - Uses external PostgreSQL with secure credentials
4. **API Keys** - Store LLM API keys in environment variables, never in code

## Extensibility

The architecture supports easy addition of new features:

- **New LLM Providers** - Extend `LLMProvider` in chat-service
- **Additional Services** - Use the same patterns for new microservices
- **Database Migrations** - Add Alembic for schema versioning
- **Analytics** - Add a separate analytics service

## Performance & Scalability

- **Async/await** - All database operations use async SQLAlchemy
- **Connection pooling** - SQLAlchemy manages database connections
- **Stateless services** - Services can be horizontally scaled
- **JWT authentication** - No session management required

## Deployment

Services can be deployed to:
- Docker containers with orchestration (Kubernetes)
- Cloud platforms (AWS ECS, Google Cloud Run, Heroku)
- Traditional servers with process managers (systemd, supervisor)

Example Docker deployment:
```dockerfile
FROM python:3.13-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ ./app/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Support

For issues or questions, refer to individual service READMEs:
- `auth-service/README.md`
- `project-service/README.md`
- `chat-service/README.md`
