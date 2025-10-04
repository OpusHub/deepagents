"""LangGraph graph definition for Copy Creator Agent.

This is the main entry point for the LangGraph Server.
"""

from deepagents import create_deep_agent, get_default_model
from examples.copy_creator.tools import (
    internet_search,
    get_validated_copies,
    get_copywriting_formulas,
    get_market_data_templates,
    get_base_copys
)
from examples.copy_creator.agents.market_research_agent import market_research_agent
from examples.copy_creator.agents.hook_strategy_agent import hook_strategy_agent
from examples.copy_creator.agents.copy_creation_agent import copy_creation_agent
from examples.copy_creator.agents.quality_assurance_agent import quality_assurance_agent


# PROMPT CONTENT PLACEHOLDER
COPY_CREATOR_INSTRUCTIONS = """
Você é o Copy Creator Agent, especializado em criar copies de marketing de alta conversão.

# Seu Fluxo de Trabalho

Quando receber uma solicitação de criação de copies, SEMPRE siga este processo:

1. **Planejamento** (use write_todos)
   - Crie uma lista de tarefas detalhada
   - Marque cada tarefa como in_progress quando começar
   - Marque como completed quando terminar

2. **Pesquisa de Mercado** (use task tool com market_research)
   - Delegue para o market_research agent
   - Aguarde análise completa de mercado, personas e competição

3. **Estratégia de Hooks** (use task tool com hook_strategy)
   - Delegue para o hook_strategy agent
   - Aguarde criação de N hooks estratégicos

4. **Criação de Copies** (use task tool com copy_creation)
   - Delegue para o copy_creation agent
   - Aguarde geração de N copies completas

5. **Garantia de Qualidade** (use task tool com quality_assurance)
   - Delegue para o quality_assurance agent
   - Aguarde auditoria e scoring

# Dados Necessários

Antes de iniciar, certifique-se de ter:
- Cliente/Empresa
- Região
- Serviço
- Ofertas
- Telefone
- Reviews/Avaliações
- Quantidade de copies (N)

Se faltar alguma informação, pergunte ao usuário.

# Importante

- Use write_todos SEMPRE no início
- Use task tool para cada sub-agent (não tente fazer você mesmo)
- Mantenha todos atualizados constantemente
- Salve tudo em arquivos usando write_file
"""


# Create the graph
graph = create_deep_agent(
    tools=[
        internet_search,
        get_validated_copies,
        get_copywriting_formulas,
        get_market_data_templates,
        get_base_copys
    ],
    instructions=COPY_CREATOR_INSTRUCTIONS,
    model=get_default_model(),
    subagents=[
        market_research_agent,
        hook_strategy_agent,
        copy_creation_agent,
        quality_assurance_agent
    ]
)
