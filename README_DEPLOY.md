# ✅ Deploy Railway - Pronto!

## 🎯 Resumo das Correções

Todos os problemas foram corrigidos! O projeto está pronto para deploy na Railway.

### Problemas Resolvidos:

1. ✅ **Conflito de nome `types/`** → Renomeado para `models/`
2. ✅ **pyproject.toml com `tests/`** → Removido
3. ✅ **Modelo Claude** → Alterado para Gemini
4. ✅ **Railway sem start command** → Dockerfile + Procfile criados

---

## 🚀 Deploy na Railway - 5 Passos

### 1. Commit e Push
```bash
git add .
git commit -m "fix: Railway deploy ready - Gemini + estrutura corrigida"
git push origin master
```

### 2. Criar Projeto na Railway
1. Acesse https://railway.app/dashboard
2. "New Project" → "Deploy from GitHub repo"
3. Selecione seu repositório
4. Branch: `master`

### 3. Configurar Variável de Ambiente
Na Railway, vá em **Variables** e adicione:
```
GOOGLE_API_KEY=sua_chave_do_gemini_aqui
```

**Obter chave:** https://makersuite.google.com/app/apikey

### 4. Deploy Automático
- Railway detecta o Dockerfile automaticamente
- Build começa automaticamente
- Aguarde 3-5 minutos

### 5. Testar
Quando deploy terminar, acesse:
```
https://seu-app.railway.app/copy_creator/playground
```

---

## 📡 Endpoints da API

Sua URL base será: `https://seu-app.railway.app`

### Endpoints Principais:

#### 1. Health Check
```bash
GET /info
```

#### 2. Interface de Teste (Browser)
```
GET /copy_creator/playground
```

#### 3. API Principal (POST)
```bash
POST /copy_creator/invoke
Content-Type: application/json

{
  "input": {
    "messages": [{
      "role": "user",
      "content": "{\"cliente\": \"Empresa ABC\", \"regiao\": \"São Paulo - Zona Sul\", \"servico\": \"Pavimentação\", \"ofertas\": \"20% desconto\", \"telefone\": \"(11) 99999-9999\", \"reviews\": \"4.9/5\", \"numero_copies\": 3}"
    }]
  }
}
```

---

## 💻 Exemplo Frontend (JavaScript)

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
          content: JSON.stringify({
            cliente: dados.cliente,
            regiao: dados.regiao,
            servico: dados.servico,
            ofertas: dados.ofertas,
            telefone: dados.telefone,
            reviews: dados.reviews,
            numero_copies: dados.numero_copies || 3
          })
        }]
      }
    })
  });

  if (!response.ok) {
    throw new Error(`Erro HTTP: ${response.status}`);
  }

  const result = await response.json();
  return result;
}

// Uso:
gerarCopies({
  cliente: "Reforma Fácil",
  regiao: "Rio de Janeiro - Barra",
  servico: "Pintura Residencial",
  ofertas: "15% desconto primeira contratação",
  telefone: "(21) 98888-7777",
  reviews: "4.8/5 - 200 avaliações",
  numero_copies: 3
})
.then(result => console.log(result))
.catch(error => console.error(error));
```

---

## 🔍 Verificar Status do Deploy

### Via cURL:
```bash
curl https://seu-app.railway.app/info
```

### Resposta esperada:
```json
{
  "name": "copy_creator",
  "description": "...",
  "endpoints": [...]
}
```

---

## 📊 Estrutura de Resposta

### Sucesso:
```json
{
  "output": {
    "messages": [
      {
        "role": "assistant",
        "content": "Copies criadas com sucesso! ..."
      }
    ]
  }
}
```

### Erro:
```json
{
  "error": "Descrição do erro",
  "detail": "..."
}
```

---

## 🐛 Troubleshooting

### Build Falha
**Logs:** Railway Dashboard → Deployments → View Logs

**Possíveis causas:**
- Dependências faltando → Já corrigido
- Conflito `types/` → Já renomeado para `models/`
- pyproject.toml → Já corrigido

### Deploy OK mas Erro 500
1. Verifique variável `GOOGLE_API_KEY` na Railway
2. Veja logs: Railway → Deployments → View Logs
3. Teste localmente:
   ```bash
   docker build -t test .
   docker run -p 8000:8000 -e GOOGLE_API_KEY=sua_chave test
   ```

### Timeout
- Aumente `healthcheckTimeout` em [railway.json](railway.json)
- Verifique se Gemini API está respondendo

---

## 📁 Arquivos Importantes

### Configuração Deploy:
- [Dockerfile](Dockerfile) - Container
- [Procfile](Procfile) - Start command
- [railway.json](railway.json) - Config Railway
- [.dockerignore](.dockerignore) - Otimização

### Código:
- [src/deepagents/model.py](src/deepagents/model.py) - Modelo Gemini
- [examples/copy_creator/graph.py](examples/copy_creator/graph.py) - Grafo principal
- [examples/copy_creator/models/](examples/copy_creator/models/) - Schemas

### Documentação:
- [RAILWAY_SETUP.md](RAILWAY_SETUP.md) - Guia completo
- [CHANGELOG_RAILWAY.md](CHANGELOG_RAILWAY.md) - Mudanças
- [README_DEPLOY.md](README_DEPLOY.md) - Este arquivo

---

## 💰 Custos

### Railway:
- **Hobby:** $5/mês + uso (suficiente para MVP)
- **Pro:** $20/mês + uso

### Google Gemini:
- **gemini-2.0-flash-exp:** GRATUITO (experimental)
- Verifique limites em: https://ai.google.dev/pricing

---

## 🔐 Segurança

- ✅ Nunca commitar `.env` com chaves
- ✅ Usar variáveis de ambiente da Railway
- ✅ HTTPS automático (Railway)
- ⚠️ Considerar adicionar autenticação para produção

---

## 📚 Documentação Adicional

- **LangGraph:** https://langchain-ai.github.io/langgraph/
- **Railway:** https://docs.railway.app
- **Gemini API:** https://ai.google.dev/docs
- **LangSmith (tracing):** https://smith.langchain.com

---

## ✨ Tudo Pronto!

1. ✅ Código corrigido
2. ✅ Dockerfile configurado
3. ✅ Modelo Gemini integrado
4. ✅ Documentação completa

**Próximo passo:** Faça o commit e push! 🚀
