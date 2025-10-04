# 🚀 PRÓXIMOS PASSOS - DEPLOY RAILWAY

## ⚠️ PROBLEMA ATUAL

A Railway está usando **cache antigo** do build. Por isso ainda aparece:
```
Error: No such command 'serve'.
```

Mesmo que o código esteja correto localmente.

---

## ✅ SOLUÇÃO RÁPIDA

### **Passo 1: Commit com Mudança Forçada**

```bash
git add .
git commit -m "fix: Force rebuild - usar langgraph dev (invalidar cache)"
git push origin master
```

Adicionei um comentário no Dockerfile para invalidar o cache.

---

### **Passo 2: Limpar Cache na Railway (IMPORTANTE)**

#### **Opção A: Via Dashboard (Recomendado)**

1. Acesse https://railway.app/dashboard
2. Clique no seu projeto
3. Vá em **"Deployments"**
4. Clique nos **"..." (3 pontos)** do deployment
5. Selecione **"Redeploy"**
6. Se houver opção **"Clear build cache"**, marque
7. Confirme

#### **Opção B: Variável de Ambiente Temporária**

1. Railway → **Variables**
2. Adicione variável temporária:
   ```
   RAILWAY_FORCE_REBUILD=true
   ```
3. Aguarde rebuild
4. Remova a variável depois

#### **Opção C: Trigger Manual**

1. Railway → **Settings**
2. **"Trigger Deploy"**
3. Isso deve pegar código mais recente

---

### **Passo 3: Verificar Logs do Build**

Durante o build, procure por:

#### ✅ **BOM (Novo Build):**
```
[ 6/10] RUN pip install --no-cache-dir ...
Collecting langchain-google-genai
Collecting langgraph-cli
Installing collected packages: ...
Successfully installed ...
```

#### ❌ **RUIM (Cache):**
```
[ 6/10] RUN pip install ... cached
[ 9/10] COPY examples/ ... cached
```

---

### **Passo 4: Verificar Logs de Runtime**

Após deploy, os logs devem mostrar:

#### ✅ **SUCESSO:**
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:XXXX
```

#### ❌ **FALHA (Cache Antigo):**
```
Error: No such command 'serve'.
```

---

## 📋 Checklist Completo

### Antes do Deploy:
- [x] Código atualizado com `langgraph dev`
- [x] Comentário adicionado para invalidar cache
- [x] Commit feito localmente
- [ ] **Push para GitHub**
- [ ] **Limpar cache na Railway**

### Configuração Railway:
- [ ] `GOOGLE_API_KEY` configurada
- [ ] Branch correto (master)
- [ ] Deploy limpo (sem cache)

### Após Deploy:
- [ ] Build sem "cached" nas etapas importantes
- [ ] Logs mostram "Uvicorn running"
- [ ] Healthcheck `/info` passa
- [ ] Endpoint responde

---

## 🎯 Comandos Rápidos

```bash
# 1. Fazer push
git add .
git commit -m "fix: Force rebuild - langgraph dev command"
git push origin master

# 2. Aguardar deploy (~1-2 min)

# 3. Testar
curl https://seu-app.railway.app/info
```

---

## 🔍 Como Saber se Funcionou

### Teste 1: Health Check
```bash
curl https://seu-app.railway.app/info
```

**Esperado:**
```json
{"status": "ok", ...}
```

### Teste 2: Logs
Procure por:
```
INFO: Uvicorn running on http://0.0.0.0:XXXX
```

**Não deve ter:**
```
Error: No such command 'serve'
```

---

## 🆘 Se Ainda Falhar

### Última Opção: Deletar e Recriar

1. Railway → Settings → **Delete Service**
2. Criar novo service:
   - **New** → **Deploy from GitHub**
   - Selecionar repositório
   - Branch: `master`
3. Configurar variável:
   ```
   GOOGLE_API_KEY=sua_chave
   ```
4. Aguardar deploy

Isso garante build completamente limpo.

---

## ✨ Resumo

**Problema:** Cache antigo com comando errado
**Solução:** Forçar rebuild limpo
**Como:** Push + Redeploy na Railway
**Resultado:** Servidor inicia com `langgraph dev` ✅

---

## 📞 Próxima Ação

**AGORA:**
1. ✅ Fazer push: `git push origin master`
2. ✅ Railway Dashboard → Redeploy (Clear cache)
3. ✅ Aguardar 1-2 minutos
4. ✅ Testar `/info` endpoint

**Deve funcionar!** 🚀
