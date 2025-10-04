#!/bin/bash

echo "========================================="
echo "Starting Copy Creator LangGraph Server"
echo "========================================="

# Debug info
echo "Working directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Files in current dir:"
ls -la

echo ""
echo "Checking langgraph installation..."
if command -v langgraph &> /dev/null; then
    echo "langgraph CLI found at: $(which langgraph)"
    langgraph --version || echo "Version check failed"
else
    echo "ERROR: langgraph CLI not found in PATH"
    echo "Attempting to find it..."
    find /usr -name "langgraph" 2>/dev/null || true
    exit 1
fi

echo ""
echo "Checking config file..."
if [ -f "langgraph.json" ]; then
    echo "langgraph.json found"
    cat langgraph.json
else
    echo "ERROR: langgraph.json NOT FOUND"
    exit 1
fi

echo ""
echo "Python path: $PYTHONPATH"
echo "PORT: ${PORT:-8000}"

if [ -n "$GOOGLE_API_KEY" ]; then
    echo "GOOGLE_API_KEY: ${GOOGLE_API_KEY:0:10}***"
else
    echo "WARNING: GOOGLE_API_KEY not set!"
fi

echo ""
echo "========================================="
echo "Starting LangGraph server on port ${PORT:-8000}..."
echo "========================================="

# Try langgraph CLI first
echo "Attempting to start with langgraph CLI..."
timeout 10 langgraph serve --host 0.0.0.0 --port ${PORT:-8000} --config langgraph.json 2>&1 &
LANGGRAPH_PID=$!

# Wait a bit to see if it starts
sleep 3

# Check if process is still running
if kill -0 $LANGGRAPH_PID 2>/dev/null; then
    echo "langgraph CLI started successfully (PID: $LANGGRAPH_PID)"
    wait $LANGGRAPH_PID
else
    echo ""
    echo "WARNING: langgraph CLI failed to start or timed out"
    echo "Falling back to direct uvicorn server..."
    echo ""

    # Fallback to Python server
    exec python server.py
fi
