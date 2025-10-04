# ✅ Correção LangGraph CLI - Railway

## Problemas Identificados e Corrigidos

### 1. **Dependências no langgraph.json** ✅

**Problema:**
```json
{
  "dependencies": ["."]  // ❌ Não funciona no container
}
```

O `"."` refere-se ao diretório atual (`/app/examples/copy_creator`), mas o pacote `deepagents` está instalado em `/app`.

**Solução:**
```json
{
  "dependencies": ["../../."]  // ✅ Aponta para /app onde está o projeto
}
```

**Arquivo:** [examples/copy_creator/langgraph.json](examples/copy_creator/langgraph.json)

---

### 2. **CMD no Dockerfile** ✅

**Problema:**
```dockerfile
CMD ["langgraph", "serve", "--port", "${PORT:-8000}"]  # ❌ Não expande variáveis
```

O formato `exec form` (`["cmd", "arg"]`) não expande variáveis de ambiente.

**Solução:**
```dockerfile
CMD sh -c "langgraph serve --host 0.0.0.0 --port ${PORT:-8000} --config langgraph.json"
```

Usa `sh -c` para permitir expansão de variáveis.

**Arquivo:** [Dockerfile](Dockerfile)

---

## 📁 Estrutura de Diretórios

```
/app/                              # WORKDIR inicial
├── pyproject.toml                 # Projeto deepagents
├── src/
│   └── deepagents/               # Pacote instalado com pip install -e .
└── examples/
    └── copy_creator/             # WORKDIR final
        ├── langgraph.json        # Config langgraph
        ├── graph.py              # Graph principal
        ├── agents/
        ├── models/
        └── tools.py
```

### langgraph.json:
```json
{
  "dependencies": ["../../."],     // ← Aponta para /app
  "graphs": {
    "copy_creator": "./graph.py:graph"  // ← Arquivo local
  }
}
```

---

## 🔧 Como o LangGraph CLI Funciona

### 1. Carrega dependências:
```bash
langgraph serve --config langgraph.json
```

### 2. Resolve `"dependencies": ["../../."]`:
- Vai para `/app/examples/copy_creator/../../.` = `/app`
- Encontra `pyproject.toml`
- Instala o pacote `deepagents` (já está instalado)

### 3. Importa o graph:
```python
# Resolve "./graph.py:graph"
from graph import graph  # Importa de /app/examples/copy_creator/graph.py
```

### 4. Inicia servidor:
```
INFO: Started server process
INFO: Application startup complete
INFO: Uvicorn running on http://0.0.0.0:8000
```

---

## ✅ Checklist de Correções

- [x] `langgraph.json` com `dependencies: ["../../."]`
- [x] Dockerfile com `CMD sh -c "..."`
- [x] `PYTHONPATH=/app` configurado
- [x] WORKDIR = `/app/examples/copy_creator`
- [x] Pacote `deepagents` instalado com `pip install -e .`

---

## 🚀 Deploy Agora

```bash
git add .
git commit -m "fix: Corrigir langgraph.json dependencies e Dockerfile CMD"
git push origin master
```

**Na Railway:**
1. Configure `GOOGLE_API_KEY`
2. Aguarde deploy
3. Logs devem mostrar:
   ```
   INFO: Uvicorn running on http://0.0.0.0:8000
   ```

---

## 🔍 Logs Esperados (Sucesso)

```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**Healthcheck `/info` deve passar!**

---

## 🐛 Se Ainda Falhar

### Erro: "Cannot import module 'graph'"
**Causa:** PYTHONPATH incorreto

**Solução:** Verifique no Dockerfile:
```dockerfile
ENV PYTHONPATH=/app:$PYTHONPATH
WORKDIR /app/examples/copy_creator
```

---

### Erro: "Package 'deepagents' not found"
**Causa:** Dependências não carregaram

**Solução:** Verifique `langgraph.json`:
```json
{
  "dependencies": ["../../."]  // Deve apontar para /app
}
```

---

### Erro: "Port already in use"
**Causa:** Porta não está usando $PORT

**Solução:** Já corrigido no CMD:
```dockerfile
CMD sh -c "langgraph serve --port ${PORT:-8000} ..."
```

---

## 📊 Diferença Antes/Depois

### ❌ Antes:
```json
// langgraph.json
{"dependencies": ["."]}  // Errado
```
```dockerfile
# Dockerfile
CMD ["langgraph", "serve", "--port", "${PORT}"]  // Variável não expande
```

### ✅ Depois:
```json
// langgraph.json
{"dependencies": ["../../."]}  // Correto - aponta para /app
```
```dockerfile
# Dockerfile
CMD sh -c "langgraph serve --port ${PORT:-8000} ..."  // Expande variável
```

---

## 🎯 Resumo

| Problema | Solução | Arquivo |
|----------|---------|---------|
| dependencies: ["."] | dependencies: ["../../."] | langgraph.json |
| CMD não expande $PORT | CMD sh -c "..." | Dockerfile |

---

## ✨ Agora Deve Funcionar!

As correções garantem que:
1. ✅ LangGraph CLI encontra o pacote `deepagents`
2. ✅ Graph é importado corretamente
3. ✅ Servidor usa a porta correta ($PORT)
4. ✅ Healthcheck `/info` passa

**Faça commit e push agora!** 🚀
