# 🔧 Troubleshooting Railway - Healthcheck Failed

## ❌ Problema: Healthcheck Failed

```
Attempt #1-8 failed with service unavailable
1/1 replicas never became healthy!
Healthcheck failed!
```

### Causa Provável
O servidor LangGraph não está iniciando corretamente ou está demorando muito para responder.

---

## ✅ Soluções

### 1. Verificar Logs da Railway

**Passos:**
1. Railway Dashboard → Seu projeto
2. Aba "Deployments"
3. Clique no deployment que falhou
4. Clique em "View Logs"

**O que procurar:**
- Erros de importação Python
- `GOOGLE_API_KEY` não configurada
- Problemas com langgraph CLI
- Erros de porta/bind

---

### 2. Verificar Variável GOOGLE_API_KEY

**Problema:** API key não configurada

**Solução:**
```bash
# Na Railway, vá em Variables e adicione:
GOOGLE_API_KEY=sua_chave_aqui
```

**Como obter chave:**
https://makersuite.google.com/app/apikey

---

### 3. Aumentar Timeout do Healthcheck

O arquivo `railway.json` já está configurado com 300 segundos (5 minutos).

Se ainda assim falhar, edite:

```json
{
  "deploy": {
    "healthcheckTimeout": 600,  // 10 minutos
    ...
  }
}
```

---

### 4. Verificar Start Command

O Dockerfile usa o script `start_server.sh` que faz diagnóstico.

**Verificar nos logs se aparece:**
```
Starting Copy Creator LangGraph Server
Working directory: /app/examples/copy_creator
✓ langgraph.json found
```

Se não aparecer, o script não está executando.

---

### 5. Testar Localmente com Docker

```bash
# Build
docker build -t copy-creator .

# Run (substitua sua chave)
docker run -p 8000:8000 \
  -e GOOGLE_API_KEY=sua_chave_do_gemini \
  copy-creator

# Em outro terminal, teste:
curl http://localhost:8000/info
```

**Deve retornar:**
```json
{
  "name": "copy_creator",
  ...
}
```

---

### 6. Verificar Path do Config

O servidor procura por `langgraph.json` no diretório atual.

**Verificar no Dockerfile:**
```dockerfile
WORKDIR /app/examples/copy_creator  # Muda para este dir
CMD ["./start_server.sh"]           # Executa aqui
```

O `langgraph.json` deve estar em `/app/examples/copy_creator/langgraph.json`

---

### 7. Desabilitar Healthcheck Temporariamente

Para debug, você pode desabilitar o healthcheck:

**railway.json:**
```json
{
  "deploy": {
    "healthcheckPath": null,  // Desabilita
    ...
  }
}
```

⚠️ **Atenção:** Só use para debug. Re-habilite depois!

---

### 8. Verificar Dependências

**Problema:** `langgraph-cli` não instalado

**Solução:** Já está no Dockerfile:
```dockerfile
RUN pip install langchain-google-genai langgraph-cli
```

**Verificar se instalou corretamente nos logs:**
```
Successfully installed langgraph-cli-x.x.x
```

---

### 9. Verificar PYTHONPATH

O Dockerfile configura:
```dockerfile
ENV PYTHONPATH=/app:$PYTHONPATH
```

Isso permite importar:
```python
from examples.copy_creator.models import ...
```

---

### 10. Erro de Import Circular (types/)

**Problema:** Se ainda tiver `types/` no código:
```
ImportError: cannot import name 'MappingProxyType' from partially initialized module 'types'
```

**Solução:** Já corrigido! Renomeado para `models/`

Verifique se o código atual tem:
```python
from examples.copy_creator.models.copy_output import CopyOutput  # ✓
# NÃO:
from examples.copy_creator.types.copy_output import CopyOutput   # ✗
```

---

## 🔍 Checklist de Debug

- [ ] GOOGLE_API_KEY configurada na Railway?
- [ ] Logs mostram "Starting Copy Creator LangGraph Server"?
- [ ] langgraph.json encontrado nos logs?
- [ ] Sem erros de importação Python?
- [ ] Porta $PORT sendo usada corretamente?
- [ ] Testou localmente com Docker?
- [ ] Healthcheck timeout suficiente (300s+)?

---

## 🚀 Se Tudo Mais Falhar

### Opção 1: Start Simples

Edite o **Dockerfile**, troque o CMD por:

```dockerfile
CMD ["python", "-m", "http.server", "8000"]
```

Se isso funcionar, o problema é com o langgraph CLI.

### Opção 2: Railway Config Manual

Na Railway, vá em Settings → Deploy:

**Start Command:**
```bash
cd /app/examples/copy_creator && langgraph serve --host 0.0.0.0 --port $PORT --config langgraph.json
```

### Opção 3: Verificar Graph

Teste o graph localmente:

```python
from examples.copy_creator.graph import graph

# Verificar se carrega sem erro
print(graph)
```

---

## 📝 Logs Esperados (Sucesso)

```
=========================================
Starting Copy Creator LangGraph Server
=========================================
Working directory: /app/examples/copy_creator
Python version: Python 3.11.x
Files in current dir:
langgraph.json
graph.py
...

✓ langgraph.json found
{
  "dependencies": ["."],
  "graphs": {
    "copy_creator": "./graph.py:graph"
  },
  "env": ".env"
}

Python path: /app:/usr/local/lib/python3.11/site-packages

PORT=8000
GOOGLE_API_KEY=AIzaSy...

=========================================
Starting LangGraph server on port 8000...
=========================================

INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## 🆘 Ainda com Problemas?

1. **Copie os logs completos** da Railway
2. **Teste o Dockerfile localmente** primeiro
3. **Verifique todas as variáveis de ambiente**
4. **Confirme que o código está na última versão** (com `models/` não `types/`)

---

## ✅ Checklist Final

Antes de fazer deploy:

```bash
# 1. Verificar estrutura
ls examples/copy_creator/models/  # Deve existir
ls examples/copy_creator/types/   # NÃO deve existir

# 2. Verificar imports
grep -r "from examples.copy_creator.types" .  # Deve retornar vazio

# 3. Build local
docker build -t test .

# 4. Run local
docker run -p 8000:8000 -e GOOGLE_API_KEY=sua_chave test

# 5. Testar
curl http://localhost:8000/info
```

Se todos passarem ✓, o deploy na Railway deve funcionar!
