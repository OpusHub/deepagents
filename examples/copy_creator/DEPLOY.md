# Deploy do Copy Creator Agent na Railway

## Pré-requisitos

1. Conta na [Railway](https://railway.app)
2. Google API Key para o Gemini

## Passo a Passo

### 1. Configurar Projeto na Railway

1. Acesse [Railway Dashboard](https://railway.app/dashboard)
2. Clique em "New Project"
3. Selecione "Deploy from GitHub repo"
4. Conecte seu repositório
5. Selecione a branch desejada

### 2. Configurar Variáveis de Ambiente

Na Railway, vá em "Variables" e adicione:

```
GOOGLE_API_KEY=sua_chave_do_google_gemini_aqui
```

Opcional (para tracing com LangSmith):
```
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=sua_chave_langsmith
LANGCHAIN_PROJECT=copy-creator-agent
```

### 3. Configurar Build Settings

**Root Directory:**
```
examples/copy_creator
```

**Build Command:** (deixe vazio - o Dockerfile cuida disso)

**Start Command:**
```
langgraph serve --host 0.0.0.0 --port $PORT --config langgraph.json
```

OU use o Procfile (já configurado)

### 4. Deploy

1. Clique em "Deploy"
2. Aguarde o build (pode levar 3-5 minutos)
3. Quando concluído, a Railway vai gerar uma URL

## Estrutura de Arquivos

```
examples/copy_creator/
├── Dockerfile          # Configuração do container
├── railway.toml        # Configuração Railway
├── Procfile           # Comando de start
├── langgraph.json     # Configuração LangGraph
├── .env.example       # Exemplo de variáveis
├── .dockerignore      # Arquivos ignorados no build
└── start.sh           # Script de inicialização alternativo
```

## Endpoints Disponíveis

Após o deploy, sua aplicação estará disponível em:
```
https://seu-app.railway.app
```

### Principais Endpoints:

- `GET /info` - Informações do grafo
- `GET /copy_creator/playground` - Interface de teste
- `POST /copy_creator/invoke` - Execução síncrona
- `POST /copy_creator/stream` - Streaming
- `POST /copy_creator/batch` - Execução em lote

## Testando o Deploy

### Usando cURL:
```bash
curl -X POST https://seu-app.railway.app/copy_creator/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "input": {
      "messages": [{
        "role": "user",
        "content": "{\"cliente\": \"Empresa ABC\", \"regiao\": \"São Paulo\", \"servico\": \"Pavimentação\", \"ofertas\": \"20% off\", \"telefone\": \"(11) 99999-9999\", \"reviews\": \"4.9/5\", \"numero_copies\": 3}"
      }]
    }
  }'
```

### Usando JavaScript:
```javascript
const response = await fetch('https://seu-app.railway.app/copy_creator/invoke', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    input: {
      messages: [{
        role: "user",
        content: JSON.stringify({
          cliente: "Empresa ABC",
          regiao: "São Paulo - Zona Sul",
          servico: "Pavimentação",
          ofertas: "20% desconto",
          telefone: "(11) 99999-9999",
          reviews: "4.9/5 - 150 avaliações",
          numero_copies: 3
        })
      }]
    }
  })
});

const result = await response.json();
console.log(result);
```

## Logs e Debugging

Para ver os logs:
1. Acesse o projeto na Railway
2. Clique na aba "Deployments"
3. Selecione o deployment ativo
4. Clique em "View Logs"

## Troubleshooting

### Build Falha
- Verifique se todas as dependências estão no `pyproject.toml`
- Confirme que o `PYTHONPATH` está correto

### Servidor não inicia
- Verifique os logs para erros
- Confirme que `GOOGLE_API_KEY` está configurada
- Teste localmente primeiro: `langgraph serve --config langgraph.json`

### Timeout nas requisições
- Aumente o `healthcheckTimeout` no `railway.toml`
- Verifique se o modelo Gemini está respondendo

### Erros de importação
- Confirme que a estrutura de diretórios está correta
- Verifique o `PYTHONPATH` no Dockerfile

## Deploy Local (Teste)

Para testar localmente antes do deploy:

```bash
# 1. Instalar dependências
cd examples/copy_creator
pip install -e ../.. langchain-google-genai langgraph-cli

# 2. Configurar .env
cp .env.example .env
# Editar .env com sua GOOGLE_API_KEY

# 3. Rodar servidor
langgraph serve --config langgraph.json

# 4. Acessar playground
# http://localhost:8000/copy_creator/playground
```

## Custos

A Railway oferece:
- **Hobby Plan:** $5/mês + uso
- **Pro Plan:** $20/mês + uso

O agente usa Gemini (Google), que tem custos separados baseados em:
- Tokens de entrada/saída
- Modelo usado (gemini-2.0-flash-exp é mais econômico)

## Próximos Passos

1. Configure domínio customizado na Railway
2. Adicione autenticação (JWT, API Keys)
3. Configure rate limiting
4. Adicione monitoramento (LangSmith, Sentry)
5. Configure backups dos arquivos gerados
