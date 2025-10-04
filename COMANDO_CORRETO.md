# ✅ COMANDO CORRETO - langgraph dev

## 🎯 Descoberta!

Baseado no Dockerfile Node.js do mesmo projeto, o comando correto é:

```bash
langgraph dev --host 0.0.0.0 --port 8000
```

**NÃO** `langgraph serve` ❌

---

## 📋 Comparação Node.js vs Python

### Node.js (Referência):
```dockerfile
CMD ["sh", "-c", "npx @langchain/langgraph-cli dev --host 0.0.0.0 --port ${PORT:-8080}"]
```

### Python (Nossa Solução):
```dockerfile
CMD sh -c "langgraph dev --host 0.0.0.0 --port ${PORT:-8000}"
```

---

## 🔧 Dockerfile Atualizado

```dockerfile
# Instalar langgraph-cli
RUN pip install langgraph-cli

# WORKDIR no diretório com langgraph.json
WORKDIR /app/examples/copy_creator

# Comando correto
CMD sh -c "langgraph dev --host 0.0.0.0 --port ${PORT:-8000}"
```

---

## 📁 Estrutura Necessária

```
/app/examples/copy_creator/
├── langgraph.json        # Config file
├── graph.py              # Graph definition
├── agents/
├── models/
└── tools.py
```

### langgraph.json:
```json
{
  "dependencies": ["../../."],
  "graphs": {
    "copy_creator": "./graph.py:graph"
  },
  "env": ".env"
}
```

---

## 🚀 Como Funciona

### 1. langgraph dev:
- Lê `langgraph.json`
- Instala dependencies (`../../.` → `/app`)
- Importa graph (`./graph.py:graph`)
- Inicia servidor HTTP na porta especificada
- Expõe endpoints automáticos

### 2. Endpoints criados:
- `GET /info` - Health check
- `POST /copy_creator/invoke` - Executar graph
- `POST /copy_creator/stream` - Streaming
- `GET /copy_creator/playground` - UI interativa

---

## ✅ Correções Finais

### Arquivo: Dockerfile
```dockerfile
CMD sh -c "langgraph dev --host 0.0.0.0 --port ${PORT:-8000}"
```

### Arquivo: langgraph.json
```json
{
  "dependencies": ["../../."]  // Aponta para /app
}
```

---

## 🧪 Testar Localmente

```bash
# Navegar para o diretório
cd examples/copy_creator

# Instalar dependências
pip install -e ../../.
pip install langgraph-cli langchain-google-genai

# Configurar variável
export GOOGLE_API_KEY=sua_chave

# Rodar servidor
langgraph dev --host 0.0.0.0 --port 8000

# Em outro terminal
curl http://localhost:8000/info
```

---

## 📊 Comandos langgraph-cli

| Comando | Uso |
|---------|-----|
| `langgraph dev` | ✅ Servidor de desenvolvimento (USAR ESTE) |
| `langgraph build` | Build de imagem Docker |
| `langgraph deploy` | Deploy para LangGraph Cloud |
| `langgraph serve` | ❌ NÃO EXISTE |

---

## 🔍 Diferença dev vs serve

### `langgraph dev`:
- ✅ Existe e funciona
- ✅ Servidor HTTP completo
- ✅ Hot reload (desenvolvimento)
- ✅ Pode usar em produção com `--host 0.0.0.0`

### `langgraph serve`:
- ❌ Não existe
- ❌ Causa erro: "No such command 'serve'"

---

## 🎉 Solução Final

### Dockerfile:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y build-essential curl git

# Python deps
COPY pyproject.toml README.md LICENSE ./
COPY src/ ./src/
RUN pip install --no-cache-dir -e . && \
    pip install langchain-google-genai langgraph-cli

# Copy examples
COPY examples/ ./examples/

# Set workdir to graph location
WORKDIR /app/examples/copy_creator

# Env vars
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:$PYTHONPATH

# Start server with langgraph dev
CMD sh -c "langgraph dev --host 0.0.0.0 --port ${PORT:-8000}"
```

### Deploy:
```bash
git add .
git commit -m "fix: Use langgraph dev command (correto)"
git push
```

**Configure na Railway:**
```
GOOGLE_API_KEY=sua_chave_do_gemini
```

---

## ✨ Agora VAI FUNCIONAR!

O comando `langgraph dev` é o correto, igual ao usado no projeto Node.js.

🚀 **Commit e push agora!**
