# OMNICHAT API Testing Guide

## Issue with Provided Token

The provided token `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3OGI3MGQ3ZS1iODUwLTRjODAtYWFjOS04NmJlOTU2ZWNjZDYiLCJleHAiOjE3Njg1ODc5MTR9.LKs_HIatACfz-emrETyYsDA0XFhzDevXv3qJZ3d-8Bw` is returning **401 Unauthorized** because:

**The JWT_SECRET used to create the token on the deployed service differs from the JWT_SECRET configured in the deployed project-service.**

### Solution: Generate Valid Token

You need to:
1. Get a valid token from the auth-service (deployed or local)
2. Use that token with project-service

## Complete API Workflow

### 1. Register User (Auth Service)

```bash
curl -X POST https://omnirouter-auth-services.onrender.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secure_password_123"
  }'
```

**Response:**
```json
{
  "id": "user-uuid",
  "email": "user@example.com"
}
```

### 2. Login (Auth Service)

```bash
curl -X POST https://omnirouter-auth-services.onrender.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "secure_password_123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### 3. Create Project (Project Service)

Use the `access_token` from login response:

```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X POST https://omnirouter-project-services.onrender.com/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AI Customer Service Bot",
    "description": "Intelligent chatbot for customer support"
  }'
```

**Response:**
```json
{
  "id": "project-uuid",
  "user_id": "user-uuid",
  "name": "AI Customer Service Bot",
  "description": "Intelligent chatbot for customer support",
  "created_at": "2024-01-16T17:25:30Z",
  "updated_at": "2024-01-16T17:25:30Z"
}
```

### 4. Create Prompt (Project Service)

```bash
PROJECT_ID="project-uuid"
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X POST https://omnirouter-project-services.onrender.com/projects/$PROJECT_ID/prompts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Customer Support System Prompt",
    "content": "You are a helpful AI customer service representative. You provide accurate, friendly, and professional support to customers."
  }'
```

**Response:**
```json
{
  "id": "prompt-uuid",
  "project_id": "project-uuid",
  "name": "Customer Support System Prompt",
  "content": "You are a helpful AI customer service representative...",
  "version": 1,
  "created_at": "2024-01-16T17:25:30Z",
  "updated_at": "2024-01-16T17:25:30Z"
}
```

### 5. List Projects

```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X GET https://omnirouter-project-services.onrender.com/projects \
  -H "Authorization: Bearer $TOKEN"
```

### 6. Get Project Details

```bash
PROJECT_ID="project-uuid"
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X GET https://omnirouter-project-services.onrender.com/projects/$PROJECT_ID \
  -H "Authorization: Bearer $TOKEN"
```

### 7. List Prompts for Project

```bash
PROJECT_ID="project-uuid"
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X GET https://omnirouter-project-services.onrender.com/projects/$PROJECT_ID/prompts \
  -H "Authorization: Bearer $TOKEN"
```

### 8. Update Project

```bash
PROJECT_ID="project-uuid"
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X PUT https://omnirouter-project-services.onrender.com/projects/$PROJECT_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Bot Name",
    "description": "Updated description"
  }'
```

### 9. Update Prompt

```bash
PROJECT_ID="project-uuid"
PROMPT_ID="prompt-uuid"
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X PUT https://omnirouter-project-services.onrender.com/projects/$PROJECT_ID/prompts/$PROMPT_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Prompt Name",
    "content": "Updated prompt content..."
  }'
```

### 10. Delete Prompt

```bash
PROJECT_ID="project-uuid"
PROMPT_ID="prompt-uuid"
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X DELETE https://omnirouter-project-services.onrender.com/projects/$PROJECT_ID/prompts/$PROMPT_ID \
  -H "Authorization: Bearer $TOKEN"
```

### 11. Delete Project

```bash
PROJECT_ID="project-uuid"
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X DELETE https://omnirouter-project-services.onrender.com/projects/$PROJECT_ID \
  -H "Authorization: Bearer $TOKEN"
```

## Chat Service API

### 1. Create Conversation

```bash
PROJECT_ID="project-uuid"
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X POST "https://omnirouter-chat-services.onrender.com/conversations?project_id=$PROJECT_ID" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
{
  "id": "conversation-uuid",
  "project_id": "project-uuid",
  "created_at": "2024-01-16T17:25:30Z",
  "updated_at": "2024-01-16T17:25:30Z"
}
```

### 2. Send Message and Get Response

```bash
CONVERSATION_ID="conversation-uuid"
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X POST "https://omnirouter-chat-services.onrender.com/conversations/$CONVERSATION_ID/messages" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Hello, I need help with my account."
  }'
```

**Response:**
```json
{
  "message_id": "conversation-uuid",
  "response": "Hello! I'd be happy to help you with your account. What specific issue are you experiencing?",
  "created_at": "2024-01-16T17:25:30Z"
}
```

### 3. Get Conversation History

```bash
CONVERSATION_ID="conversation-uuid"
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X GET "https://omnirouter-chat-services.onrender.com/conversations/$CONVERSATION_ID/messages" \
  -H "Authorization: Bearer $TOKEN"
```

### 4. List Project Conversations

```bash
PROJECT_ID="project-uuid"
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X GET "https://omnirouter-chat-services.onrender.com/conversations/project/$PROJECT_ID" \
  -H "Authorization: Bearer $TOKEN"
```

### 5. Get Conversation Details

```bash
CONVERSATION_ID="conversation-uuid"
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X GET "https://omnirouter-chat-services.onrender.com/conversations/$CONVERSATION_ID" \
  -H "Authorization: Bearer $TOKEN"
```

### 6. Delete Conversation

```bash
CONVERSATION_ID="conversation-uuid"
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X DELETE "https://omnirouter-chat-services.onrender.com/conversations/$CONVERSATION_ID" \
  -H "Authorization: Bearer $TOKEN"
```

## PowerShell Test Script

Save this as `test-api.ps1`:

```powershell
# Configuration
$AUTH_URL = "https://omnirouter-auth-services.onrender.com"
$PROJECT_URL = "https://omnirouter-project-services.onrender.com"
$CHAT_URL = "https://omnirouter-chat-services.onrender.com"

$email = "test@example.com"
$password = "TestPassword123!"

# Step 1: Register
Write-Host "1. Registering user..." -ForegroundColor Cyan
$registerResponse = Invoke-WebRequest -Uri "$AUTH_URL/auth/register" `
    -Method POST `
    -ContentType "application/json" `
    -Body (@{ email = $email; password = $password } | ConvertTo-Json)

$userId = ($registerResponse.Content | ConvertFrom-Json).id
Write-Host "User registered: $userId" -ForegroundColor Green

# Step 2: Login
Write-Host "`n2. Logging in..." -ForegroundColor Cyan
$loginResponse = Invoke-WebRequest -Uri "$AUTH_URL/auth/login" `
    -Method POST `
    -ContentType "application/json" `
    -Body (@{ email = $email; password = $password } | ConvertTo-Json)

$token = ($loginResponse.Content | ConvertFrom-Json).access_token
Write-Host "Token received: $($token.Substring(0, 20))..." -ForegroundColor Green

$headers = @{ Authorization = "Bearer $token"; "Content-Type" = "application/json" }

# Step 3: Create Project
Write-Host "`n3. Creating project..." -ForegroundColor Cyan
$projectResponse = Invoke-WebRequest -Uri "$PROJECT_URL/projects" `
    -Method POST `
    -Headers $headers `
    -Body (@{ 
        name = "Test Bot"
        description = "A test chatbot project" 
    } | ConvertTo-Json)

$projectId = ($projectResponse.Content | ConvertFrom-Json).id
Write-Host "Project created: $projectId" -ForegroundColor Green

# Step 4: Create Prompt
Write-Host "`n4. Creating prompt..." -ForegroundColor Cyan
$promptResponse = Invoke-WebRequest -Uri "$PROJECT_URL/projects/$projectId/prompts" `
    -Method POST `
    -Headers $headers `
    -Body (@{
        name = "System Prompt"
        content = "You are a helpful assistant."
    } | ConvertTo-Json)

$promptId = ($promptResponse.Content | ConvertFrom-Json).id
Write-Host "Prompt created: $promptId" -ForegroundColor Green

# Step 5: Create Conversation
Write-Host "`n5. Creating conversation..." -ForegroundColor Cyan
$conversationResponse = Invoke-WebRequest -Uri "$CHAT_URL/conversations?project_id=$projectId" `
    -Method POST `
    -Headers $headers

$conversationId = ($conversationResponse.Content | ConvertFrom-Json).id
Write-Host "Conversation created: $conversationId" -ForegroundColor Green

# Step 6: Send Message
Write-Host "`n6. Sending message..." -ForegroundColor Cyan
$messageResponse = Invoke-WebRequest -Uri "$CHAT_URL/conversations/$conversationId/messages" `
    -Method POST `
    -Headers $headers `
    -Body (@{ content = "Hello, how are you?" } | ConvertTo-Json)

$response = ($messageResponse.Content | ConvertFrom-Json).response
Write-Host "AI Response: $response" -ForegroundColor Green

Write-Host "`n✅ All tests completed successfully!" -ForegroundColor Yellow
```

## Environment URLs

- **Auth Service:** https://omnirouter-auth-services.onrender.com
- **Project Service:** https://omnirouter-project-services.onrender.com
- **Chat Service:** https://omnirouter-chat-services.onrender.com

## Troubleshooting

### 401 Unauthorized
- **Cause:** Invalid or expired token
- **Solution:** Generate a new token by logging in with valid credentials

### 404 Not Found
- **Cause:** Project/prompt/conversation doesn't exist or was already deleted
- **Solution:** Verify the UUID is correct

### 500 Internal Server Error
- **Cause:** LLM API issue (chat service) or database connection issue
- **Solution:** Check that LLM API keys are configured and database is accessible

### Missing Authorization Header
- **Cause:** Forgot to include `Authorization: Bearer <token>` header
- **Solution:** Add the header to all requests (except register/login)
