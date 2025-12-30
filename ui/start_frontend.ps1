# PowerShell script to start the React frontend development server

# Function to kill existing processes on port 3000
function Kill-Port3000 {
    Write-Host "Checking for processes on port 3000..."
    $process = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue
    if ($process) {
        $processId = $process.OwningProcess
    Write-Host "Killing process on port 3000 (PID: $processId)"
    Stop-Process -Id $processId -Force
    } else {
        Write-Host "No process found on port 3000"
    }
}

# Kill any existing process on port 3000
Kill-Port3000

# Change to frontend directory
Set-Location -Path "frontend"

# Start the React development server
Write-Host "Starting React development server..."
npm start