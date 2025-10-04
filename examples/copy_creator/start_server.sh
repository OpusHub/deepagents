#!/bin/bash
set -e

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
which langgraph || echo "langgraph CLI not found in PATH"

echo ""
echo "Checking config file..."
if [ -f "langgraph.json" ]; then
    echo "✓ langgraph.json found"
    cat langgraph.json
else
    echo "✗ langgraph.json NOT FOUND"
    exit 1
fi

echo ""
echo "Python path:"
echo $PYTHONPATH

echo ""
echo "Environment variables:"
echo "PORT=${PORT:-8000}"
echo "GOOGLE_API_KEY=${GOOGLE_API_KEY:0:10}..." # Show only first 10 chars

echo ""
echo "========================================="
echo "Starting LangGraph server on port ${PORT:-8000}..."
echo "========================================="

# Start server
exec langgraph serve --host 0.0.0.0 --port ${PORT:-8000} --config langgraph.json
