# Configuration - Local Services
$AUTH_URL = "http://localhost:8000"
$PROJECT_URL = "http://localhost:8001"
$CHAT_URL = "http://localhost:8002"

$email = "testuser_$(Get-Random)@example.com"
$password = "TestPassword123!"

Write-Host "`n================================" -ForegroundColor Cyan
Write-Host "OMNICHAT Local API Test" -ForegroundColor Cyan
Write-Host "================================`n" -ForegroundColor Cyan

Write-Host "Services expected at:" -ForegroundColor Yellow
Write-Host "  Auth Service: $AUTH_URL" -ForegroundColor Yellow
Write-Host "  Project Service: $PROJECT_URL" -ForegroundColor Yellow
Write-Host "  Chat Service: $CHAT_URL" -ForegroundColor Yellow
Write-Host "`nMake sure to start the services:" -ForegroundColor Cyan
Write-Host "  cd auth-service; python -m uvicorn app.main:app --port 8000" -ForegroundColor Cyan
Write-Host "  cd project-service; python -m uvicorn app.main:app --port 8001" -ForegroundColor Cyan
Write-Host "  cd chat-service; python -m uvicorn app.main:app --port 8002" -ForegroundColor Cyan
Write-Host ""

try {
    # Step 1: Register
    Write-Host "1. Registering user..." -ForegroundColor Cyan
    $registerResponse = Invoke-WebRequest -Uri "$AUTH_URL/auth/register" `
        -Method POST `
        -ContentType "application/json" `
        -Body (@{ email = $email; password = $password } | ConvertTo-Json) `
        -ErrorAction Stop

    $userId = ($registerResponse.Content | ConvertFrom-Json).id
    Write-Host "✅ User registered: $userId`n" -ForegroundColor Green

    # Step 2: Login
    Write-Host "2. Logging in..." -ForegroundColor Cyan
    $loginResponse = Invoke-WebRequest -Uri "$AUTH_URL/auth/login" `
        -Method POST `
        -ContentType "application/json" `
        -Body (@{ email = $email; password = $password } | ConvertTo-Json) `
        -ErrorAction Stop

    $token = ($loginResponse.Content | ConvertFrom-Json).access_token
    Write-Host "✅ Login successful`n" -ForegroundColor Green
    Write-Host "Token: $($token.Substring(0, 30))...`n" -ForegroundColor Yellow

    $headers = @{ Authorization = "Bearer $token"; "Content-Type" = "application/json" }

    # Step 3: Create Project
    Write-Host "3. Creating project..." -ForegroundColor Cyan
    $projectResponse = Invoke-WebRequest -Uri "$PROJECT_URL/projects" `
        -Method POST `
        -Headers $headers `
        -Body (@{ 
            name = "AI Customer Service Bot"
            description = "Intelligent chatbot for customer support" 
        } | ConvertTo-Json) `
        -ErrorAction Stop

    $project = $projectResponse.Content | ConvertFrom-Json
    $projectId = $project.id
    Write-Host "✅ Project created`n" -ForegroundColor Green
    Write-Host "Project ID: $projectId" -ForegroundColor Yellow
    Write-Host "Name: $($project.name)" -ForegroundColor Yellow
    Write-Host "Description: $($project.description)`n" -ForegroundColor Yellow

    # Step 4: Create Prompt
    Write-Host "4. Creating prompt..." -ForegroundColor Cyan
    $promptResponse = Invoke-WebRequest -Uri "$PROJECT_URL/projects/$projectId/prompts" `
        -Method POST `
        -Headers $headers `
        -Body (@{
            name = "Customer Support System Prompt"
            content = "You are a helpful AI customer service representative. You provide accurate, friendly, and professional support to customers."
        } | ConvertTo-Json) `
        -ErrorAction Stop

    $prompt = $promptResponse.Content | ConvertFrom-Json
    $promptId = $prompt.id
    Write-Host "✅ Prompt created`n" -ForegroundColor Green
    Write-Host "Prompt ID: $promptId" -ForegroundColor Yellow
    Write-Host "Name: $($prompt.name)" -ForegroundColor Yellow
    Write-Host "Version: $($prompt.version)`n" -ForegroundColor Yellow

    # Step 5: List Projects
    Write-Host "5. Listing projects..." -ForegroundColor Cyan
    $projectsResponse = Invoke-WebRequest -Uri "$PROJECT_URL/projects" `
        -Method GET `
        -Headers $headers `
        -ErrorAction Stop

    $projects = $projectsResponse.Content | ConvertFrom-Json
    Write-Host "✅ Projects retrieved: $($projects.Count) project(s)`n" -ForegroundColor Green

    # Step 6: Get Project Details
    Write-Host "6. Getting project details..." -ForegroundColor Cyan
    $detailResponse = Invoke-WebRequest -Uri "$PROJECT_URL/projects/$projectId" `
        -Method GET `
        -Headers $headers `
        -ErrorAction Stop

    $details = $detailResponse.Content | ConvertFrom-Json
    Write-Host "✅ Project details retrieved`n" -ForegroundColor Green
    Write-Host "Updated at: $($details.updated_at)`n" -ForegroundColor Yellow

    # Step 7: List Prompts
    Write-Host "7. Listing prompts..." -ForegroundColor Cyan
    $promptsResponse = Invoke-WebRequest -Uri "$PROJECT_URL/projects/$projectId/prompts" `
        -Method GET `
        -Headers $headers `
        -ErrorAction Stop

    $prompts = $promptsResponse.Content | ConvertFrom-Json
    Write-Host "✅ Prompts retrieved: $($prompts.Count) prompt(s)`n" -ForegroundColor Green

    # Step 8: Create Conversation
    Write-Host "8. Creating conversation..." -ForegroundColor Cyan
    $conversationResponse = Invoke-WebRequest -Uri "$CHAT_URL/conversations?project_id=$projectId" `
        -Method POST `
        -Headers $headers `
        -ErrorAction Stop

    $conversation = $conversationResponse.Content | ConvertFrom-Json
    $conversationId = $conversation.id
    Write-Host "✅ Conversation created`n" -ForegroundColor Green
    Write-Host "Conversation ID: $conversationId`n" -ForegroundColor Yellow

    # Step 9: Send Message (if LLM is configured)
    Write-Host "9. Sending message..." -ForegroundColor Cyan
    try {
        $messageResponse = Invoke-WebRequest -Uri "$CHAT_URL/conversations/$conversationId/messages" `
            -Method POST `
            -Headers $headers `
            -Body (@{ content = "Hello, I need help with my account." } | ConvertTo-Json) `
            -ErrorAction Stop

        $messageResult = $messageResponse.Content | ConvertFrom-Json
        Write-Host "✅ Message sent and response received`n" -ForegroundColor Green
        Write-Host "AI Response:`n$($messageResult.response)`n" -ForegroundColor Yellow
    }
    catch {
        Write-Host "⚠️ Message sending failed (LLM may not be configured)" -ForegroundColor Yellow
        Write-Host "Error: $($_.Exception.Message)`n" -ForegroundColor Yellow
    }

    # Step 10: Get Conversation History
    Write-Host "10. Getting conversation history..." -ForegroundColor Cyan
    $historyResponse = Invoke-WebRequest -Uri "$CHAT_URL/conversations/$conversationId/messages" `
        -Method GET `
        -Headers $headers `
        -ErrorAction Stop

    $messages = $historyResponse.Content | ConvertFrom-Json
    Write-Host "✅ Conversation history retrieved: $($messages.Count) message(s)`n" -ForegroundColor Green

    # Step 11: List Project Conversations
    Write-Host "11. Listing project conversations..." -ForegroundColor Cyan
    $conversationsResponse = Invoke-WebRequest -Uri "$CHAT_URL/conversations/project/$projectId" `
        -Method GET `
        -Headers $headers `
        -ErrorAction Stop

    $allConversations = $conversationsResponse.Content | ConvertFrom-Json
    Write-Host "✅ Project conversations retrieved: $($allConversations.Count) conversation(s)`n" -ForegroundColor Green

    Write-Host "================================" -ForegroundColor Cyan
    Write-Host "✅ All API tests completed successfully!" -ForegroundColor Green
    Write-Host "================================`n" -ForegroundColor Cyan

    Write-Host "Summary:" -ForegroundColor Cyan
    Write-Host "  User Email: $email" -ForegroundColor Yellow
    Write-Host "  User ID: $userId" -ForegroundColor Yellow
    Write-Host "  Project ID: $projectId" -ForegroundColor Yellow
    Write-Host "  Prompt ID: $promptId" -ForegroundColor Yellow
    Write-Host "  Conversation ID: $conversationId" -ForegroundColor Yellow
    Write-Host ""
}
catch {
    Write-Host "`n❌ Error occurred:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Make sure all services are running on the correct ports" -ForegroundColor Yellow
    Write-Host "2. Run each service in a separate terminal:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Terminal 1 - Auth Service:" -ForegroundColor Cyan
    Write-Host "  cd F:\OMNICHAT\auth-service" -ForegroundColor Cyan
    Write-Host "  python -m uvicorn app.main:app --host 0.0.0.0 --port 8000" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Terminal 2 - Project Service:" -ForegroundColor Cyan
    Write-Host "  cd F:\OMNICHAT\project-service" -ForegroundColor Cyan
    Write-Host "  python -m uvicorn app.main:app --host 0.0.0.0 --port 8001" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Terminal 3 - Chat Service:" -ForegroundColor Cyan
    Write-Host "  cd F:\OMNICHAT\chat-service" -ForegroundColor Cyan
    Write-Host "  python -m uvicorn app.main:app --host 0.0.0.0 --port 8002" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Then run this script:" -ForegroundColor Cyan
    Write-Host "  .\test-api-local.ps1" -ForegroundColor Cyan
}
