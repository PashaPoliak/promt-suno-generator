#!/bin/bash
kill_port_3000() {
    echo "Checking for processes on port 3000..."
    PID=$(lsof -ti:3000)
    if [ ! -z "$PID" ]; then
        echo "Killing process on port 3000 (PID: $PID)"
        kill -9 $PID
    else
        echo "No process found on port 3000"
    fi
}

kill_port_3000

echo "Starting React development server..."
npm start