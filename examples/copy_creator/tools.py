"""Custom tools for Copy Creator agent."""

import os
from pathlib import Path
from langchain_core.tools import tool
from typing import Optional


# Get current directory for relative paths
CURRENT_DIR = Path(__file__).parent
KNOWLEDGE_BASE_DIR = CURRENT_DIR / "knowledge-base"


@tool
def internet_search(query: str, max_results: int = 5) -> str:
    """
    Search the internet using Tavily API.

    Args:
        query: Search query
        max_results: Maximum number of results

    Returns:
        Search results as formatted string
    """
    # TODO: Implement Tavily API integration
    # This is a placeholder implementation
    return f"Search results for: {query}\n(Tavily API integration needed)"


@tool
def get_validated_copies() -> str:
    """
    Acessa a base de conhecimento com 17 copies validadas de alta conversão para referência na criação de novas copies.
    Use esta ferramenta SEMPRE antes de criar copies.

    Returns:
        Validated copies database
    """
    file_path = KNOWLEDGE_BASE_DIR / "validated-copies.md"

    if not file_path.exists():
        return "Arquivo de copies validadas não encontrado. Verifique se o arquivo validated-copies.md existe na pasta knowledge-base."

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Erro ao ler arquivo de copies validadas: {str(e)}"


@tool
def get_copywriting_formulas() -> str:
    """
    Acessa fórmulas validadas de copywriting, gatilhos psicológicos, estruturas de 30-40 segundos e padrões de linguagem convertedora.
    Essencial para criar copies seguindo padrões testados.

    Returns:
        Copywriting formulas (AIDA, PAS, etc.)
    """
    file_path = KNOWLEDGE_BASE_DIR / "copywriting-formulas.md"

    if not file_path.exists():
        return "Arquivo de fórmulas de copywriting não encontrado. Verifique se o arquivo copywriting-formulas.md existe na pasta knowledge-base."

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Erro ao ler arquivo de fórmulas: {str(e)}"


@tool
def get_market_data_templates() -> str:
    """
    Acessa templates para análise de mercado, criação de personas, análise competitiva e insights comportamentais
    específicos para o setor de construção e home improvement.

    Returns:
        Market analysis templates
    """
    file_path = KNOWLEDGE_BASE_DIR / "market-data-templates.md"

    if not file_path.exists():
        return "Arquivo de templates de mercado não encontrado. Verifique se o arquivo market-data-templates.md existe na pasta knowledge-base."

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Erro ao ler templates de mercado: {str(e)}"


@tool
def get_base_copys() -> str:
    """
    Acessa o arquivo base-copys.md que contém exemplos detalhados de copies com transcrições e descrições.
    Use para referência visual e estrutural.

    Returns:
        Reference copy database
    """
    file_path = CURRENT_DIR / "base-copys.md"

    if not file_path.exists():
        return "Arquivo base-copys.md não encontrado. Verifique se o arquivo existe na pasta copy_creator."

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Erro ao ler base-copys.md: {str(e)}"
