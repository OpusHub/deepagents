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

# Copiar arquivos de dependências
COPY pyproject.toml ./
COPY src/ ./src/
COPY examples/copy_creator/ ./examples/copy_creator/

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e . && \
    pip install --no-cache-dir langchain-google-genai langgraph-cli

# Expor porta do LangGraph Server
EXPOSE 8000

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV LANGSERVE_GRAPHS='{"copy_creator": "examples.copy_creator.graph:graph"}'

# Comando para iniciar o LangGraph Server
CMD ["langgraph", "serve", "--host", "0.0.0.0", "--port", "8000", "--config", "examples/copy_creator/langgraph.json"]
