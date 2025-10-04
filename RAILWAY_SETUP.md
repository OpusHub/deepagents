# 🚀 Deploy na Railway - Guia Completo

## ✅ Correções Aplicadas

1. **pyproject.toml** corrigido - removida referência ao diretório `tests/`
2. **Dockerfile** otimizado na raiz do projeto
3. **Procfile** e **railway.json** configurados

## 📋 Pré-requisitos

- [ ] Conta na [Railway](https://railway.app)
- [ ] Google API Key para Gemini ([Obter aqui](https://makersuite.google.com/app/apikey))
- [ ] Repositório Git com o código

## 🔧 Configuração na Railway

### Passo 1: Criar Novo Projeto

1. Acesse [Railway Dashboard](https://railway.app/dashboard)
2. Clique em **"New Project"**
3. Selecione **"Deploy from GitHub repo"**
4. Conecte seu repositório
5. Selecione a branch `master` (ou sua branch principal)

### Passo 2: Configurar Build

Na Railway, vá em **Settings → Build**:

```
Build Method: Dockerfile
Dockerfile Path: Dockerfile
Build Context: . (raiz)
```

A Railway vai detectar automaticamente o Dockerfile na raiz.

### Passo 3: Variáveis de Ambiente

Vá em **Variables** e adicione:

#### Obrigatória:
```bash
GOOGLE_API_KEY=sua_chave_do_google_gemini_aqui
```

#### Opcionais (LangSmith para tracing):
```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=sua_chave_langsmith
LANGCHAIN_PROJECT=copy-creator-agent
```

### Passo 4: Deploy

1. Clique em **"Deploy"**
2. Aguarde o build (3-5 minutos primeira vez)
3. Railway vai gerar uma URL automaticamente
4. Acesse: `https://seu-app.railway.app/copy_creator/playground`

## 🧪 Testando o Deploy

### Verificar Status
```bash
curl https://seu-app.railway.app/info
```

### Testar Endpoint Principal
```bash
curl -X POST https://seu-app.railway.app/copy_creator/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "messages": [{
        "role": "user",
        "content": "{\"cliente\": \"Test Co\", \"regiao\": \"São Paulo\", \"servico\": \"Pavimentação\", \"ofertas\": \"20% off\", \"telefone\": \"(11) 99999-9999\", \"reviews\": \"4.9/5\", \"numero_copies\": 3}"
      }]
    }
  }'
```

### Usando JavaScript (Frontend)
```javascript
const API_URL = 'https://seu-app.railway.app';

async function criarCopies() {
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
            cliente: "Empresa ABC",
            regiao: "São Paulo - Zona Sul",
            servico: "Pavimentação",
            ofertas: "20% desconto primeiros 10 clientes",
            telefone: "(11) 98765-4321",
            reviews: "4.9/5 - 150 avaliações",
            numero_copies: 3
          })
        }]
      }
    })
  });

  const result = await response.json();
  console.log(result);
  return result;
}
```

## 📊 Endpoints Disponíveis

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/info` | GET | Informações do grafo |
| `/copy_creator/playground` | GET | Interface de teste visual |
| `/copy_creator/invoke` | POST | Execução síncrona (recomendado) |
| `/copy_creator/stream` | POST | Streaming em tempo real |
| `/copy_creator/batch` | POST | Processamento em lote |

## 🐛 Troubleshooting

### Problema: Build Falha

**Erro: `package directory 'tests' does not exist`**

✅ **Solução:** Já corrigido no commit mais recente. Faça pull das mudanças.

---

**Erro: `ModuleNotFoundError: No module named 'langchain_google_genai'`**

✅ **Solução:** Já incluído no Dockerfile. Verifique se está usando a versão mais recente.

---

### Problema: Servidor não Inicia

**Erro: `GOOGLE_API_KEY not found`**

✅ **Solução:** Configure a variável de ambiente na Railway:
```bash
GOOGLE_API_KEY=sua_chave_aqui
```

---

**Erro: `Port already in use`**

✅ **Solução:** A Railway automaticamente define `$PORT`. Não precisa configurar.

---

### Problema: Timeout nas Requisições

**Erro: `Gateway timeout 504`**

✅ **Solução:**
1. Aumente o `healthcheckTimeout` em `railway.json`
2. Verifique os logs da Railway
3. Teste o endpoint `/info` para ver se o servidor está respondendo

---

### Problema: Resposta Vazia ou Erro 500

**Verificar logs:**
1. Acesse Railway Dashboard
2. Clique no projeto
3. Vá em "Deployments" → Deployment ativo → "View Logs"

**Possíveis causas:**
- Modelo Gemini não está respondendo (verifique API key)
- Formato de entrada incorreto (veja exemplos acima)
- Falta de dependências (já corrigido)

## 📈 Monitoramento

### Ver Logs em Tempo Real
1. Railway Dashboard → Seu Projeto
2. Aba "Deployments"
3. Clique no deployment ativo
4. "View Logs"

### Métricas
- CPU/RAM: Railway Dashboard → Metrics
- Requisições: Use LangSmith (se configurado)

## 💰 Custos Estimados

### Railway
- **Hobby Plan:** $5/mês + $0.000231/GB-hora
- **Pro Plan:** $20/mês + uso adicional

### Google Gemini API
- **gemini-2.0-flash-exp:**
  - Input: Gratuito (experimental)
  - Output: Gratuito (experimental)

*Nota: Preços podem mudar. Verifique a documentação oficial.*

## 🔒 Segurança

### Recomendações:
1. ✅ Nunca commitar `.env` com API keys
2. ✅ Use variáveis de ambiente da Railway
3. ✅ Considere adicionar autenticação (JWT, API Keys)
4. ✅ Configure rate limiting se necessário
5. ✅ Use HTTPS (Railway faz automaticamente)

## 🎯 Próximos Passos

- [ ] Configurar domínio customizado
- [ ] Adicionar autenticação
- [ ] Configurar CI/CD automático
- [ ] Adicionar rate limiting
- [ ] Configurar backup de dados
- [ ] Integrar com LangSmith para observabilidade

## 📚 Recursos Adicionais

- [Railway Docs](https://docs.railway.app)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [Gemini API Docs](https://ai.google.dev/docs)
- [LangSmith](https://smith.langchain.com)

## 🆘 Suporte

Se encontrar problemas:
1. Verifique os logs da Railway
2. Teste localmente primeiro: `docker build -t test . && docker run -p 8000:8000 test`
3. Abra uma issue no repositório
