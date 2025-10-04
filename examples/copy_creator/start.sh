#!/bin/bash

# Script de inicialização para Railway
echo "Iniciando Copy Creator Agent..."

# Usar porta do Railway ou padrão 8000
PORT=${PORT:-8000}

echo "Porta: $PORT"
echo "Config: langgraph.json"

# Iniciar LangGraph Server
exec langgraph serve --host 0.0.0.0 --port $PORT --config langgraph.json
