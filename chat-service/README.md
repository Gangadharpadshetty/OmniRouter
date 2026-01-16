# Chat Service

The Chat Service handles conversations and chat interactions with LLM providers (OpenAI or OpenRouter).

## Features

- Create conversations
- Send messages and get LLM responses
- Maintain conversation history
- Support for multiple LLM providers (OpenRouter, OpenAI)
- Automatic message storage

## Architecture

```
app/
├── core/
│   ├── config.py          # Configuration settings
│   ├── database.py        # Database setup
│   └── security.py        # JWT token verification
├── domain/
│   └── chat.py            # Domain models
├── repositories/
│   ├── chat_repository.py       # Repository protocols
│   └── postgres_chat_repo.py    # PostgreSQL implementation
├── services/
│   ├── chat_service.py          # Business logic
│   └── llm_provider.py          # LLM provider abstraction
├── routes/
│   └── chat.py            # API endpoints
├── schemas/
│   └── chat.py            # Pydantic models
├── utils/
│   └── dependencies.py    # Dependency injection
└── main.py                # FastAPI app
```

## Running the Service

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```
DATABASE_URL=postgresql://user:password@localhost:5432/omnichat
JWT_SECRET=your-secret-key
LLM_PROVIDER=openrouter
LLM_MODEL=openai/gpt-3.5-turbo
OPENROUTER_API_KEY=your-key
OPENAI_API_KEY=your-key  # optional
```

3. Run the service:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8002
```

## API Endpoints

### Conversations

- `POST /conversations?project_id={id}` - Create a new conversation
- `GET /conversations/{id}` - Get conversation details
- `GET /conversations/{id}/messages` - Get conversation history
- `DELETE /conversations/{id}` - Delete conversation
- `GET /conversations/project/{project_id}` - List project conversations

### Messages

- `POST /conversations/{conversation_id}/messages` - Send message and get response

## LLM Providers

### OpenRouter
- Default provider
- Supports multiple models
- Set `LLM_PROVIDER=openrouter` and provide `OPENROUTER_API_KEY`

### OpenAI
- Set `LLM_PROVIDER=openai` and provide `OPENAI_API_KEY`
- Model format: `gpt-3.5-turbo`, `gpt-4`, etc.

## Authentication

All endpoints require a JWT token in the `Authorization` header:
```
Authorization: Bearer <token>
```

## Message Format

Send a message:
```json
POST /conversations/conversation-id/messages
{
  "content": "Hello, how are you?"
}
```

Response:
```json
{
  "message_id": "conversation-id",
  "response": "I'm doing well, thank you for asking!",
  "created_at": "2024-01-16T12:00:00"
}
```
