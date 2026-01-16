# OMNICHAT Architecture & Design

## System Design

OMNICHAT is built as a microservices architecture with three independent services that communicate through REST APIs and share a common database.

### Design Principles

1. **Separation of Concerns** - Each service has a specific responsibility
2. **Stateless Services** - Services don't maintain state; all state is in the database
3. **Scalability** - Services use async/await and connection pooling for high concurrency
4. **Security** - JWT-based authentication with shared secret across services
5. **Extensibility** - Plugin architecture for LLM providers

## Service Architecture

### Layered Architecture (Per Service)

Each service follows a layered architecture:

```
Routes (API Endpoints)
      ↓
Schemas (Request/Response Models)
      ↓
Dependencies (Dependency Injection)
      ↓
Services (Business Logic)
      ↓
Repositories (Data Access)
      ↓
Domain Models (Entity Definitions)
      ↓
Core (Config, Database, Security)
```

### Layer Descriptions

#### Core Layer
- **Config** - Environment variables and application settings
- **Database** - SQLAlchemy async engine and session factory
- **Security** - JWT token verification and hashing

#### Domain Layer
- Pure Python dataclasses representing business entities
- No external dependencies
- Used by services and repositories

#### Repository Layer
- Abstract protocols defining data access interfaces
- PostgreSQL implementations using SQLAlchemy ORM
- Handles all database operations

#### Service Layer
- Business logic and orchestration
- Calls repositories to access data
- No HTTP or database concerns

#### Schema Layer
- Pydantic models for request/response validation
- Automatic OpenAPI documentation
- Type hints for IDE support

#### Route Layer
- FastAPI route handlers
- HTTP status codes and error handling
- Dependency injection integration

## Data Flow

### User Registration & Login Flow

```
Client
  ↓
[POST /auth/register] → Auth Service Routes
  ↓
dependencies.get_auth_service()
  ↓
AuthService.register()
  ↓
MySQLUserRepository.create()
  ↓
UserTable → PostgreSQL
  ↓
User domain model → Response Schema
  ↓
Client receives response
```

### Project Creation Flow

```
Client (with JWT)
  ↓
[POST /projects] → Project Service Routes
  ↓
get_current_user(authorization header)
  ↓
verify_token() → Extract user_id
  ↓
get_project_service(db)
  ↓
ProjectService.create_project()
  ↓
PostgresProjectRepository.create()
  ↓
ProjectTable → PostgreSQL
  ↓
Project domain model → Response Schema
  ↓
Client receives response
```

### Chat Message Flow

```
Client (with JWT)
  ↓
[POST /conversations/{id}/messages] → Chat Service Routes
  ↓
get_current_user() → Extract user_id
  ↓
get_message_service(db)
  ↓
MessageService.send_message_and_get_response()
  ↓
1. Save user message → PostgreSQL
  ↓
2. Fetch conversation history → PostgreSQL
  ↓
3. Call LLM Provider (OpenRouter/OpenAI)
  ↓
4. Save assistant response → PostgreSQL
  ↓
Response Schema
  ↓
Client receives response
```

## Database Schema

### Users Table
```sql
users (auth-service)
├── id (UUID, PK)
├── email (VARCHAR, UNIQUE)
├── password_hash (VARCHAR)
├── created_at (TIMESTAMP)
└── is_active (BOOLEAN)
```

### Projects & Prompts
```sql
projects (project-service)
├── id (UUID, PK)
├── user_id (UUID, FK to users)
├── name (VARCHAR)
├── description (VARCHAR)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

prompts (project-service)
├── id (UUID, PK)
├── project_id (UUID, FK to projects)
├── name (VARCHAR)
├── content (VARCHAR)
├── version (INTEGER)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)
```

### Conversations & Messages
```sql
conversations (chat-service)
├── id (UUID, PK)
├── project_id (UUID)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

messages (chat-service)
├── id (UUID, PK)
├── conversation_id (UUID, FK to conversations)
├── role (VARCHAR: 'user' or 'assistant')
├── content (VARCHAR)
└── created_at (TIMESTAMP)
```

## Authentication & Authorization

### JWT Token Structure
```json
{
  "sub": "user-uuid",
  "exp": 1234567890,
  "iat": 1234567800
}
```

### Token Flow
1. Client authenticates with Auth Service
2. Auth Service returns JWT token
3. Client includes token in Authorization header: `Bearer <token>`
4. Each service verifies token signature using shared `JWT_SECRET`
5. Extract `sub` claim to get `user_id`

### Authorization Levels
- **Authentication** - Token must be valid and not expired
- **Authorization** - User can only access their own resources

Example: User cannot access another user's projects
```python
# In project_service repositories
async def get_by_id(self, project_id: str, user_id: str) -> Project | None:
    # user_id parameter enforces user isolation
    result = await self.db.execute(
        select(ProjectTable).where(
            (ProjectTable.id == uuid.UUID(project_id)) & 
            (ProjectTable.user_id == uuid.UUID(user_id))
        )
    )
```

## Scalability Considerations

### Horizontal Scaling
- **Stateless Services** - Each instance is independent
- **Load Balancer** - Route requests to multiple instances
- **Database Pooling** - SQLAlchemy handles connection pooling

### Vertical Scaling
- **Async Operations** - All I/O is non-blocking
- **Connection Limits** - Configure pool_size in database config
- **Memory Management** - Dataclass-based models are lightweight

### Performance Optimizations
1. **Database Indexes** - Add indexes on frequently queried columns
   ```sql
   CREATE INDEX idx_projects_user_id ON projects(user_id);
   CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
   ```

2. **Caching** - Add Redis for prompt caching
3. **Batch Operations** - Optimize bulk queries
4. **Query Optimization** - Use select() with specific columns

## LLM Provider Architecture

### Provider Interface
```python
class LLMProvider(ABC):
    @abstractmethod
    async def send_message(self, messages: List[LLMMessage]) -> str:
        pass
```

### Supported Providers
1. **OpenRouter** - Multi-model support, good pricing
2. **OpenAI** - Official OpenAI API access

### Adding New Provider
1. Create new class extending `LLMProvider`
2. Implement `send_message()` method
3. Update `get_llm_provider()` factory function
4. Add configuration to environment variables

Example:
```python
class AnthropicProvider(LLMProvider):
    async def send_message(self, messages: List[LLMMessage]) -> str:
        # Implementation
        pass
```

## Error Handling

### HTTP Status Codes
- **200 OK** - Successful request
- **400 Bad Request** - Invalid input
- **401 Unauthorized** - Missing or invalid token
- **404 Not Found** - Resource not found
- **500 Internal Server Error** - Server error

### Exception Handling
```python
@router.post("/projects")
async def create_project(...):
    try:
        project = await service.create_project(...)
        return ProjectResponse(...)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal error")
```

## Security Best Practices

1. **Password Hashing** - Use pbkdf2_sha256 via passlib
2. **JWT Secrets** - Use strong, random secrets (40+ characters)
3. **HTTPS** - Always use HTTPS in production
4. **API Keys** - Store in environment variables, never in code
5. **Database Credentials** - Use environment variables
6. **User Isolation** - Enforce at repository level
7. **Input Validation** - Use Pydantic for automatic validation

## Testing Strategy

### Unit Tests
- Test services in isolation with mocked repositories
- Test repository implementations with test database

### Integration Tests
- Test complete flows through all layers
- Use PostgreSQL test containers

### E2E Tests
- Test complete workflows across services
- Include authentication and LLM calls

## Deployment Architecture

### Docker Deployment
```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app/ ./app/
ENV PYTHONUNBUFFERED=1
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  auth-service:
    image: omnichat-auth:latest
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: ${DATABASE_URL}
      JWT_SECRET: ${JWT_SECRET}

  project-service:
    image: omnichat-project:latest
    ports:
      - "8001:8000"
    depends_on:
      - auth-service

  chat-service:
    image: omnichat-chat:latest
    ports:
      - "8002:8000"
    depends_on:
      - auth-service
    environment:
      OPENROUTER_API_KEY: ${OPENROUTER_API_KEY}
```

### Kubernetes Deployment
- Use StatefulSets for services
- Use ConfigMaps for configuration
- Use Secrets for sensitive data
- Load balancing with Services

## Future Enhancements

1. **File Upload Support** - Integrate OpenAI Files API
2. **Analytics Service** - Track usage and conversations
3. **Rate Limiting** - Prevent abuse with Redis
4. **Caching Layer** - Redis for prompt and response caching
5. **WebSocket Support** - Real-time chat updates
6. **Multi-tenancy** - Support multiple organizations
7. **API Gateway** - Kong or similar for unified API
8. **Message Queue** - Celery/RabbitMQ for async tasks
9. **Monitoring** - Prometheus, Grafana integration
10. **Logging** - ELK stack for centralized logging
