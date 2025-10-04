# 🔄 FORÇAR REBUILD NA RAILWAY

## ❌ Problema

A Railway está usando **build em cache** e não pegou as últimas mudanças:

```
[ 6/10] RUN pip install ... cached  ← CACHE ANTIGO
[ 9/10] COPY examples/copy_creator/start_server.sh ./ cached  ← CACHE ANTIGO
```

Por isso ainda está executando comando antigo:
```
Error: No such command 'serve'.
```

---

## ✅ Solução: Forçar Rebuild

### Opção 1: Via Railway Dashboard (RECOMENDADO)

1. Acesse [Railway Dashboard](https://railway.app/dashboard)
2. Clique no seu projeto
3. Aba **"Deployments"**
4. Clique nos 3 pontinhos **"..."** do deployment ativo
5. Selecione **"Redeploy"**
6. Marque opção **"Clear build cache"** (se disponível)
7. Confirme

---

### Opção 2: Modificar Dockerfile

Adicione uma linha de comentário para forçar invalidar cache:

```dockerfile
# Force rebuild: 2025-01-04-v2
CMD sh -c "langgraph dev --host 0.0.0.0 --port ${PORT:-8000} --no-browser"
```

Depois:
```bash
git add Dockerfile
git commit -m "chore: Force rebuild"
git push
```

---

### Opção 3: Commit Vazio

Force um novo commit:
```bash
git commit --allow-empty -m "chore: Force Railway rebuild"
git push
```

---

## 🔍 Como Verificar se Pegou as Mudanças

Nos logs do build, procure por:

### ❌ Cache (Ruim):
```
[ 6/10] RUN pip install ... cached
```

### ✅ Novo Build (Bom):
```
[ 6/10] RUN pip install ...
Installing collected packages: ...
Successfully installed ...
```

---

## 📋 Verificar se Commit Está no Railway

1. Railway Dashboard → Settings → Source
2. Verifique se está apontando para:
   - **Branch:** `master`
   - **Latest commit:** Deve ser o seu commit mais recente

Se não estiver, force um push:
```bash
git push origin master --force
```

---

## 🚨 Se Ainda Não Funcionar

### Deletar e Recriar Deploy

1. Railway Dashboard → Settings
2. **"Delete Service"** (só o service, não o projeto)
3. Criar novo service:
   - New → Deploy from GitHub
   - Selecionar repo
   - Branch: master
4. Configurar variáveis novamente:
   ```
   GOOGLE_API_KEY=sua_chave
   ```

---

## ✅ Após Rebuild

Logs devem mostrar:
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Não deve aparecer:**
```
Error: No such command 'serve'.  ← Isso significa cache antigo!
```

---

## 🎯 Verificação Final

Seu Dockerfile ATUAL deve ter:
```dockerfile
CMD sh -c "langgraph dev --host 0.0.0.0 --port ${PORT:-8000} --no-browser"
```

**NÃO:**
```dockerfile
CMD ["./start_server.sh"]  # ← Antigo
CMD ["python", "server.py"]  # ← Antigo
CMD sh -c "langgraph serve ..."  # ← Antigo
```

Se o arquivo local está correto mas Railway usa cache, use uma das opções acima para forçar rebuild!

---

## 📝 Resumo

1. ✅ Código local está correto (`langgraph dev`)
2. ❌ Railway está usando cache com código antigo
3. 🔄 Solução: **Forçar rebuild sem cache**

**Método mais rápido:** Opção 1 - Redeploy via Dashboard
