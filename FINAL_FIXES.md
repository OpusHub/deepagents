# 🔧 Correções Finais - Healthcheck Railway

## ❌ Problema Identificado

```
Healthcheck failed!
Attempt #1-8 failed with service unavailable
```

**Causa:** Servidor LangGraph não estava iniciando corretamente.

---

## ✅ Correções Aplicadas

### 1. **Script de Diagnóstico** ✅
Criado: [examples/copy_creator/start_server.sh](examples/copy_creator/start_server.sh)

```bash
#!/bin/bash
# Mostra debug info antes de iniciar servidor
# - Working directory
# - Python version
# - Arquivos presentes
# - Config langgraph.json
# - Variáveis de ambiente
```

**Benefício:** Logs detalhados para debug na Railway

---

### 2. **Dockerfile Atualizado** ✅
Arquivo: [Dockerfile](Dockerfile)

**Mudança:**
```dockerfile
# Antes:
CMD ["sh", "-c", "langgraph serve ..."]

# Depois:
COPY examples/copy_creator/start_server.sh ./
RUN chmod +x start_server.sh
CMD ["./start_server.sh"]
```

**Benefício:** Script bash dedicado com melhor error handling

---

### 3. **Railway.json Ajustado** ✅
Arquivo: [railway.json](railway.json)

**Mudanças:**
```json
{
  "deploy": {
    "startCommand": "langgraph serve --host 0.0.0.0 --port $PORT --config langgraph.json",
    "healthcheckTimeout": 300,  // Aumentado de 100 para 300s
    ...
  }
}
```

**Benefício:**
- Start command correto (sem path absoluto)
- Timeout maior para primeira inicialização

---

### 4. **Troubleshooting Guide** ✅
Criado: [TROUBLESHOOT_RAILWAY.md](TROUBLESHOOT_RAILWAY.md)

10 soluções detalhadas para problemas comuns:
- Verificar logs
- Configurar GOOGLE_API_KEY
- Aumentar timeout
- Testar localmente
- Debug de imports
- etc.

---

## 🎯 Checklist Antes do Deploy

### ✅ Arquivos Criados/Atualizados:
- [x] Dockerfile com start_server.sh
- [x] start_server.sh com debug
- [x] railway.json com timeout 300s
- [x] Procfile correto
- [x] TROUBLESHOOT_RAILWAY.md

### ✅ Estrutura Corrigida:
- [x] `types/` renomeado para `models/`
- [x] Todos imports atualizados
- [x] pyproject.toml sem `tests/`
- [x] Modelo alterado para Gemini

### ✅ Configuração Railway:
- [ ] GOOGLE_API_KEY configurada (fazer manualmente)
- [x] Dockerfile na raiz
- [x] Healthcheck path: `/info`
- [x] Timeout: 300s

---

## 🚀 Próximos Passos

### 1. Commit e Push
```bash
git add .
git commit -m "fix: Adicionar debug script e corrigir healthcheck Railway"
git push origin master
```

### 2. Na Railway
1. Aguardar novo deploy automático
2. **IMPORTANTE:** Configure `GOOGLE_API_KEY` nas variáveis
3. Observe os logs durante deploy

### 3. Verificar Logs
Procure por:
```
Starting Copy Creator LangGraph Server
✓ langgraph.json found
Starting LangGraph server on port 8000...
```

### 4. Testar Endpoints
Quando deploy concluir:
```bash
# Health check
curl https://seu-app.railway.app/info

# Playground (browser)
https://seu-app.railway.app/copy_creator/playground
```

---

## 🐛 Se Ainda Falhar

### Debug Rápido:
1. **Veja os logs completos** na Railway
2. **Procure por** "ERRO", "Error", "Failed"
3. **Verifique** se `GOOGLE_API_KEY` aparece nos logs (primeiros 10 chars)

### Possíveis Problemas:

#### A. GOOGLE_API_KEY não configurada
```
Logs: "GOOGLE_API_KEY=..."
```
Se vazio, adicione na Railway Variables

#### B. Erro de importação
```
ModuleNotFoundError: No module named 'examples.copy_creator.types'
```
Significa que ainda tem import antigo (types em vez de models)

#### C. langgraph CLI não encontrado
```
langgraph: command not found
```
Problema no Dockerfile - mas já foi corrigido

#### D. Timeout muito curto
```
Healthcheck failed after 300s
```
Aumente timeout em railway.json para 600

---

## 📊 Como Deve Funcionar

### 1. Build (Railway)
```
✓ Dockerfile detected
✓ Dependencies installed
✓ deepagents package installed
✓ langchain-google-genai installed
✓ langgraph-cli installed
Build time: ~30s
```

### 2. Deploy (Railway)
```
✓ Container started
✓ start_server.sh executed
✓ Debug info printed
✓ LangGraph server started on $PORT
✓ Healthcheck /info OK
Deploy successful!
```

### 3. Runtime (Produção)
```
POST /copy_creator/invoke
→ Recebe dados do cliente
→ Executa agentes (market_research, hook_strategy, etc)
→ Retorna copies geradas
```

---

## 🔍 Teste Local Completo

Antes de fazer deploy, teste localmente:

```bash
# 1. Build
docker build -t copy-creator-test .

# 2. Run
docker run -p 8000:8000 \
  -e GOOGLE_API_KEY=sua_chave_real_aqui \
  copy-creator-test

# 3. Em outro terminal - Health check
curl http://localhost:8000/info

# 4. Teste completo
curl -X POST http://localhost:8000/copy_creator/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "messages": [{
        "role": "user",
        "content": "{\"cliente\": \"Test\", \"regiao\": \"SP\", \"servico\": \"Teste\", \"ofertas\": \"10%\", \"telefone\": \"11-9999\", \"reviews\": \"5/5\", \"numero_copies\": 1}"
      }]
    }
  }'
```

**Resultado esperado:** JSON com copies geradas

---

## 📝 Resumo das Mudanças

| Arquivo | Mudança | Motivo |
|---------|---------|--------|
| Dockerfile | + start_server.sh | Debug detalhado |
| railway.json | timeout 300s | Primeira inicialização lenta |
| railway.json | startCommand fix | Path correto após WORKDIR |
| start_server.sh | Novo arquivo | Diagnóstico + start |
| TROUBLESHOOT_RAILWAY.md | Novo guia | Debug completo |

---

## ✅ Tudo Pronto!

**Arquivos principais:**
- ✅ [Dockerfile](Dockerfile) - Build otimizado + debug
- ✅ [railway.json](railway.json) - Config corrigida
- ✅ [start_server.sh](examples/copy_creator/start_server.sh) - Start com debug
- ✅ [TROUBLESHOOT_RAILWAY.md](TROUBLESHOOT_RAILWAY.md) - Guia de troubleshooting

**Próximo commit:**
```bash
git add .
git commit -m "fix: Add debug script and fix Railway healthcheck"
git push
```

**Não esqueça:**
- Configure `GOOGLE_API_KEY` na Railway
- Observe os logs durante deploy
- Teste `/info` endpoint primeiro

🚀 Boa sorte com o deploy!
