# Test script for Project Service
Write-Host "Testing Project Service..." -ForegroundColor Cyan

# Configuration
$AUTH_URL = "https://omnirouter-auth1.onrender.com"
$PROJECT_URL = "https://omnirouter-project-services.onrender.com"

# Test 1: Check service health
Write-Host "`n1. Testing Project Service Health..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "$PROJECT_URL/health" -Method Get
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
    Write-Host "Response: $($_.Exception.Response | ConvertTo-Json)" -ForegroundColor Red
    exit 1
}

# Test 3: Get projects with token
Write-Host "`n3. Testing GET /projects..." -ForegroundColor Yellow
try {
    $headers = @{
        "Authorization" = "Bearer $token"
        "Content-Type" = "application/json"
    }
    
    $projects = Invoke-RestMethod -Uri "$PROJECT_URL/projects" -Method Get -Headers $headers
    Write-Host "✓ Successfully retrieved projects!" -ForegroundColor Green
    Write-Host "Projects count: $($projects.Count)" -ForegroundColor Gray
    if ($projects.Count -gt 0) {
        Write-Host "Sample project: $($projects[0] | ConvertTo-Json)" -ForegroundColor Gray
    }
} catch {
    Write-Host "✗ Failed to get projects: $_" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $reader.BaseStream.Position = 0
        $responseBody = $reader.ReadToEnd()
        Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
        Write-Host "Response Body: $responseBody" -ForegroundColor Red
    }
}

# Test 4: Create a test project
Write-Host "`n4. Testing POST /projects (create project)..." -ForegroundColor Yellow
try {
    $headers = @{
        "Authorization" = "Bearer $token"
        "Content-Type" = "application/json"
    }
    
    $newProject = @{
        name = "Test Project $(Get-Date -Format 'HHmmss')"
        description = "Test project created by diagnostic script"
    } | ConvertTo-Json
    
    $created = Invoke-RestMethod -Uri "$PROJECT_URL/projects" -Method Post -Headers $headers -Body $newProject
    Write-Host "✓ Successfully created project!" -ForegroundColor Green
    Write-Host "Project ID: $($created.id)" -ForegroundColor Gray
    Write-Host "Project Name: $($created.name)" -ForegroundColor Gray
} catch {
    Write-Host "✗ Failed to create project: $_" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $reader.BaseStream.Position = 0
        $responseBody = $reader.ReadToEnd()
        Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
        Write-Host "Response Body: $responseBody" -ForegroundColor Red
    }
}

Write-Host "`n=== Test Complete ===" -ForegroundColor Cyan
