# Test script for Chat Service
Write-Host "Testing Chat Service..." -ForegroundColor Cyan

# Configuration
$AUTH_URL = "https://omnirouter-auth1.onrender.com"
$PROJECT_URL = "https://omnirouter-project-services.onrender.com"
$CHAT_URL = "https://omnirouter-chatservice.onrender.com"

# Test 1: Check service health
Write-Host "`n1. Testing Chat Service Health..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "$CHAT_URL/health" -Method Get
    Write-Host "✓ Health check passed: $($health | ConvertTo-Json)" -ForegroundColor Green
} catch {
    Write-Host "✗ Health check failed: $_" -ForegroundColor Red
    Write-Host "Response: $($_.Exception.Response)" -ForegroundColor Red
}

# Test 2: Login to get token
Write-Host "`n2. Logging in to get auth token..." -ForegroundColor Yellow
Write-Host "Enter your email: " -NoNewline
$email = Read-Host
Write-Host "Enter your password: " -NoNewline
$password = Read-Host -AsSecureString
$passwordPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))

try {
    $loginBody = @{
        email = $email
        password = $passwordPlain
    } | ConvertTo-Json

    $loginResponse = Invoke-RestMethod -Uri "$AUTH_URL/auth/login" -Method Post -Body $loginBody -ContentType "application/json"
    $token = $loginResponse.access_token
    Write-Host "✓ Login successful!" -ForegroundColor Green
    Write-Host "Token: $($token.Substring(0, 20))..." -ForegroundColor Gray
} catch {
    Write-Host "✗ Login failed: $_" -ForegroundColor Red
    exit 1
}

# Test 3: Get or create a project
Write-Host "`n3. Getting projects..." -ForegroundColor Yellow
try {
    $headers = @{
        "Authorization" = "Bearer $token"
        "Content-Type" = "application/json"
    }
    
    $projects = Invoke-RestMethod -Uri "$PROJECT_URL/projects" -Method Get -Headers $headers
    
    if ($projects.Count -eq 0) {
        Write-Host "No projects found. Creating test project..." -ForegroundColor Yellow
        $newProject = @{
            name = "Chat Test Project"
            description = "Test project for chat service"
        } | ConvertTo-Json
        
        $project = Invoke-RestMethod -Uri "$PROJECT_URL/projects" -Method Post -Headers $headers -Body $newProject
        Write-Host "✓ Created test project: $($project.id)" -ForegroundColor Green
    } else {
        $project = $projects[0]
        Write-Host "✓ Using existing project: $($project.id)" -ForegroundColor Green
    }
} catch {
    Write-Host "✗ Failed to get/create project: $_" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $reader.BaseStream.Position = 0
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response: $responseBody" -ForegroundColor Red
    }
    exit 1
}

# Test 4: Create a conversation
Write-Host "`n4. Testing POST /conversations (create conversation)..." -ForegroundColor Yellow
try {
    $headers = @{
        "Authorization" = "Bearer $token"
        "Content-Type" = "application/json"
    }
    
    $conversationUrl = "$CHAT_URL/conversations?project_id=$($project.id)"
    $conversation = Invoke-RestMethod -Uri $conversationUrl -Method Post -Headers $headers
    Write-Host "✓ Successfully created conversation!" -ForegroundColor Green
    Write-Host "Conversation ID: $($conversation.id)" -ForegroundColor Gray
} catch {
    Write-Host "✗ Failed to create conversation: $_" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $reader.BaseStream.Position = 0
        $responseBody = $reader.ReadToEnd()
        Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
        Write-Host "Response Body: $responseBody" -ForegroundColor Red
    }
    exit 1
}

# Test 5: Send a message
Write-Host "`n5. Testing POST /conversations/{id}/messages (send message)..." -ForegroundColor Yellow
try {
    $headers = @{
        "Authorization" = "Bearer $token"
        "Content-Type" = "application/json"
    }
    
    $messageBody = @{
        content = "Hello! This is a test message. Please respond with 'Test successful'."
    } | ConvertTo-Json
    
    $messageUrl = "$CHAT_URL/conversations/$($conversation.id)/messages"
    Write-Host "Sending message to: $messageUrl" -ForegroundColor Gray
    
    $messageResponse = Invoke-RestMethod -Uri $messageUrl -Method Post -Headers $headers -Body $messageBody
    Write-Host "✓ Successfully sent message and got response!" -ForegroundColor Green
    Write-Host "Response: $($messageResponse.response.Substring(0, [Math]::Min(200, $messageResponse.response.Length)))..." -ForegroundColor Gray
} catch {
    Write-Host "✗ Failed to send message: $_" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $reader.BaseStream.Position = 0
        $responseBody = $reader.ReadToEnd()
        Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
        Write-Host "Response Body: $responseBody" -ForegroundColor Red
    }
}

# Test 6: Get conversation messages
Write-Host "`n6. Testing GET /conversations/{id}/messages (get messages)..." -ForegroundColor Yellow
try {
    $headers = @{
        "Authorization" = "Bearer $token"
    }
    
    $messagesUrl = "$CHAT_URL/conversations/$($conversation.id)/messages"
    $messages = Invoke-RestMethod -Uri $messagesUrl -Method Get -Headers $headers
    Write-Host "✓ Successfully retrieved messages!" -ForegroundColor Green
    Write-Host "Message count: $($messages.Count)" -ForegroundColor Gray
    
    foreach ($msg in $messages) {
        Write-Host "  [$($msg.role)]: $($msg.content.Substring(0, [Math]::Min(80, $msg.content.Length)))..." -ForegroundColor Gray
    }
} catch {
    Write-Host "✗ Failed to get messages: $_" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $reader.BaseStream.Position = 0
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response: $responseBody" -ForegroundColor Red
    }
}

# Test 7: List project conversations
Write-Host "`n7. Testing GET /conversations/project/{id} (list conversations)..." -ForegroundColor Yellow
try {
    $headers = @{
        "Authorization" = "Bearer $token"
    }
    
    $listUrl = "$CHAT_URL/conversations/project/$($project.id)"
    $conversations = Invoke-RestMethod -Uri $listUrl -Method Get -Headers $headers
    Write-Host "✓ Successfully listed conversations!" -ForegroundColor Green
    Write-Host "Conversation count: $($conversations.Count)" -ForegroundColor Gray
} catch {
    Write-Host "✗ Failed to list conversations: $_" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $reader.BaseStream.Position = 0
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response: $responseBody" -ForegroundColor Red
    }
}

Write-Host "`n=== Test Complete ===" -ForegroundColor Cyan
