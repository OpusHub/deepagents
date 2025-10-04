# 🚀 DEPLOY RAILWAY - GUIA FINAL

## ✅ Tudo Resolvido!

### Problemas Corrigidos:
1. ✅ Modelo alterado: Claude → **Gemini 2.0 Flash**
2. ✅ Conflito `types/` → Renomeado para **`models/`**
3. ✅ pyproject.toml → Referência a `tests/` removida
4. ✅ Comando langgraph → **`langgraph dev`** (não `serve`)
5. ✅ langgraph.json → `dependencies: ["../../."]`
6. ✅ Dockerfile → CMD correto com variável `$PORT`

---

## 📋 Configuração Final

### 1. **Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Dependências do sistema
RUN apt-get update && apt-get install -y build-essential curl git && \
    rm -rf /var/lib/apt/lists/*

# Copiar e instalar pacote Python
COPY pyproject.toml README.md LICENSE ./
COPY src/ ./src/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e . && \
    pip install --no-cache-dir langchain-google-genai langgraph-cli

# Copiar aplicação
COPY examples/ ./examples/

# Mudar para diretório do agent
WORKDIR /app/examples/copy_creator

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:$PYTHONPATH

# Iniciar servidor LangGraph
CMD sh -c "langgraph dev --host 0.0.0.0 --port ${PORT:-8000} --no-browser"
```

### 2. **langgraph.json**
```json
{
  "dependencies": ["../../."],
  "graphs": {
    "copy_creator": "./graph.py:graph"
  },
  "env": ".env"
}
```

### 3. **src/deepagents/model.py**
```python
from langchain_google_genai import ChatGoogleGenerativeAI

def get_default_model():
    return ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp", temperature=0.7)
```

---

## 🎯 Estrutura de Diretórios

```
/app/                                # Raiz
├── pyproject.toml                  # Define pacote deepagents
├── src/deepagents/
│   └── model.py                    # Gemini configurado
└── examples/
    └── copy_creator/               # WORKDIR do container
        ├── langgraph.json          # Config
        ├── graph.py                # Graph principal
        ├── agents/
        ├── models/                 # ← Renomeado (era types/)
        └── tools.py
```

---

## 🚀 Como Fazer Deploy

### **Passo 1: Commit e Push**
```bash
git add .
git commit -m "fix: Configuração completa Railway - Gemini + langgraph dev"
git push origin master
```

### **Passo 2: Railway - Variável de Ambiente**
Acesse [Railway Dashboard](https://railway.app/dashboard) e configure:

```
GOOGLE_API_KEY=sua_chave_do_gemini_aqui
```

**Obter chave:** https://makersuite.google.com/app/apikey

### **Passo 3: Aguardar Deploy**
- Build: ~30 segundos
- Deploy: ~15 segundos
- Total: ~1 minuto

### **Passo 4: Testar**
```bash
# Health check
curl https://seu-app.railway.app/info

# Deve retornar:
# {"status": "ok", ...}
```

---

## 📡 Endpoints da API

**Base URL:** `https://seu-app.railway.app`

### 1. Health Check
```bash
GET /info
```

### 2. Executar Agent (Principal)
```bash
POST /copy_creator/invoke

Content-Type: application/json

{
  "input": {
    "messages": [{
      "role": "user",
      "content": "{\"cliente\":\"Empresa ABC\",\"regiao\":\"São Paulo\",\"servico\":\"Pavimentação\",\"ofertas\":\"20% off\",\"telefone\":\"(11) 99999-9999\",\"reviews\":\"4.9/5\",\"numero_copies\":3}"
    }]
  }
}
```

### 3. Streaming
```bash
POST /copy_creator/stream
```

### 4. Playground (Browser)
```
GET /copy_creator/playground
```

---

## 💻 Exemplo Frontend

```javascript
const API_URL = 'https://seu-app.railway.app';

async function gerarCopies(dados) {
  const response = await fetch(`${API_URL}/copy_creator/invoke`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      input: {
        messages: [{
          role: "user",
          content: JSON.stringify(dados)
        }]
      }
    })
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const result = await response.json();
  return result;
}

// Uso
gerarCopies({
  cliente: "Reforma Rápida",
  regiao: "São Paulo - Zona Sul",
  servico: "Pavimentação de Calçadas",
  ofertas: "20% desconto primeiros 10 clientes",
  telefone: "(11) 98765-4321",
  reviews: "4.9/5 - 150 avaliações Google",
  numero_copies: 3
})
.then(result => console.log(result))
.catch(error => console.error('Erro:', error));
```

---

## 🔍 Logs na Railway

**Ver logs:**
1. Railway Dashboard → Seu Projeto
2. Aba "Deployments"
3. Click no deployment ativo
4. "View Logs"

**Logs esperados (sucesso):**
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## 🐛 Troubleshooting

### Healthcheck Failed
**Verifique:**
- ✅ `GOOGLE_API_KEY` configurada na Railway?
- ✅ Logs mostram "Uvicorn running"?
- ✅ Porta correta ($PORT)?

### Erro de Import
```
ModuleNotFoundError: No module named 'examples.copy_creator.types'
```
**Solução:** Ainda tem import antigo. Deve ser `.models` não `.types`

### Timeout
**Solução:** Aumentar `healthcheckTimeout` em `railway.json` para 600

---

## 📊 Comandos langgraph-cli

| Comando | Descrição |
|---------|-----------|
| `langgraph dev` | ✅ Servidor de desenvolvimento (USAR ESTE) |
| `langgraph build` | Build de imagem Docker |
| `langgraph up` | Servidor em modo produção (requer Docker) |
| `langgraph deploy` | Deploy para LangGraph Cloud |

**Não existe:** `langgraph serve` ❌

---

## ✅ Checklist Final

### Antes do Deploy:
- [x] Código com `models/` (não `types/`)
- [x] pyproject.toml sem `tests/`
- [x] Modelo Gemini configurado
- [x] Dockerfile com `langgraph dev`
- [x] langgraph.json com `dependencies: ["../../."]`
- [ ] **GOOGLE_API_KEY configurada na Railway**

### Após Deploy:
- [ ] Build completou com sucesso
- [ ] Logs mostram "Uvicorn running"
- [ ] `/info` endpoint responde
- [ ] Testar `/copy_creator/invoke`

---

## 💰 Custos Estimados

### Railway:
- **Hobby Plan:** $5/mês + uso
- Uso estimado: $2-5/mês adicional (app pequeno)

### Google Gemini:
- **gemini-2.0-flash-exp:** Gratuito (experimental)
- Quando sair da fase experimental: ~$0.00015/1K tokens

**Total estimado:** ~$7-10/mês

---

## 📚 Documentação

- **LangGraph Docs:** https://langchain-ai.github.io/langgraph/
- **LangGraph CLI:** https://docs.langchain.com/langgraph-platform/cli
- **Railway Docs:** https://docs.railway.app
- **Gemini API:** https://ai.google.dev/docs

---

## 🎉 Pronto!

Todos os problemas foram resolvidos. O deploy deve funcionar agora!

### **Faça o commit e push:**
```bash
git add .
git commit -m "fix: Configuração final Railway - langgraph dev + Gemini"
git push origin master
```

### **Configure na Railway:**
```
GOOGLE_API_KEY=sua_chave_aqui
```

### **Aguarde o deploy e teste:**
```bash
curl https://seu-app.railway.app/info
```

🚀 **Boa sorte!**
