# Setup Labelit to run automatically using Task Scheduler
# This is more reliable than Startup folder

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Labelit Auto-Start Setup (Task Scheduler)" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get AWS credentials from current session or AWS config
$awsKeyId = $env:AWS_ACCESS_KEY_ID
$awsSecretKey = $env:AWS_SECRET_ACCESS_KEY
$awsRegion = if ($env:AWS_REGION) { $env:AWS_REGION } else { "us-east-1" }

# If not in environment, try to get from AWS config
if (-not $awsKeyId) {
    Write-Host "Checking for AWS credentials..." -ForegroundColor Yellow
    
    $awsConfigPath = "$env:USERPROFILE\.aws\credentials"
    if (Test-Path $awsConfigPath) {
        Write-Host "Found AWS credentials file" -ForegroundColor Green
        $awsKeyId = "FROM_AWS_CONFIG"
        $awsSecretKey = "FROM_AWS_CONFIG"
    } else {
        Write-Host "ERROR: AWS credentials not found!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please set AWS credentials first:" -ForegroundColor Yellow
        Write-Host "  Option 1: Run 'aws configure'" -ForegroundColor White
        Write-Host "  Option 2: Set environment variables:" -ForegroundColor White
        Write-Host '    $env:AWS_ACCESS_KEY_ID="your_key"' -ForegroundColor Gray
        Write-Host '    $env:AWS_SECRET_ACCESS_KEY="your_secret"' -ForegroundColor Gray
        Write-Host ""
        Write-Host "Then run this script again." -ForegroundColor Yellow
        exit 1
    }
}

# Create the startup script
$startupScript = @"
@echo off
REM Labelit Auto-Start Script

REM AWS credentials will be loaded from ~/.aws/credentials automatically
REM Or you can set them here:
REM set AWS_ACCESS_KEY_ID=your_key
REM set AWS_SECRET_ACCESS_KEY=your_secret
REM set AWS_REGION=us-east-1

REM Change to user directory
cd /d "%USERPROFILE%"

REM Start Labelit
labelit start

REM If labelit exits, wait before closing
timeout /t 5 /nobreak
"@

$scriptPath = "$env:USERPROFILE\.labelit\start_labelit.bat"
$startupScript | Out-File -FilePath $scriptPath -Encoding ASCII

Write-Host "Created startup script: $scriptPath" -ForegroundColor Green

# Create Task Scheduler task
$taskName = "Labelit Screenshot Renamer"
$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c `"$scriptPath`"" -WorkingDirectory "$env:USERPROFILE"

$trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME

$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -ExecutionTimeLimit (New-TimeSpan -Hours 0) `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1)

# Unregister existing task if it exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "Removing existing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Register the task
try {
    Register-ScheduledTask `
        -TaskName $taskName `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Description "Automatically renames screenshots using AI" `
        -Force | Out-Null
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "SUCCESS! Auto-start configured!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Labelit will now start automatically when you log in." -ForegroundColor White
    Write-Host ""
    Write-Host "To test it now:" -ForegroundColor Yellow
    Write-Host "  1. Open Task Scheduler (taskschd.msc)" -ForegroundColor White
    Write-Host "  2. Find 'Labelit Screenshot Renamer'" -ForegroundColor White
    Write-Host "  3. Right-click -> Run" -ForegroundColor White
    Write-Host "  4. Take a screenshot to test!" -ForegroundColor White
    Write-Host ""
    Write-Host "Or just restart your computer." -ForegroundColor White
    Write-Host ""
    Write-Host "To remove auto-start:" -ForegroundColor Gray
    Write-Host "  Unregister-ScheduledTask -TaskName '$taskName' -Confirm:`$false" -ForegroundColor Gray
    
} catch {
    Write-Host "ERROR: Failed to create scheduled task" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "You may need to run PowerShell as Administrator" -ForegroundColor Yellow
}
