# Dockerfile para deploy do Copy Creator Agent na Railway
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de configuração primeiro
COPY pyproject.toml README.md LICENSE ./
COPY src/ ./src/

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e . && \
    pip install --no-cache-dir langchain-google-genai langgraph-cli langserve[all] uvicorn fastapi

# Copiar o resto do projeto
COPY examples/ ./examples/

# Mudar para o diretório do copy_creator
WORKDIR /app/examples/copy_creator

# Copiar e preparar script de start
COPY examples/copy_creator/start_server.sh ./
RUN chmod +x start_server.sh

# Expor porta do LangGraph Server
EXPOSE 8000

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:$PYTHONPATH

# Comando para iniciar o LangGraph Server
# langgraph dev procura langgraph.json automaticamente no diretório atual
# Updated: 2025-01-04 - Usando langgraph dev (não serve)
CMD sh -c "langgraph dev --host 0.0.0.0 --port ${PORT:-8000} --no-browser"
