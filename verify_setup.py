#!/usr/bin/env python3
"""
Script de verificação para deploy Railway.
Executa antes do deploy para garantir que tudo está correto.
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath: str) -> bool:
    """Verifica se arquivo existe."""
    exists = Path(filepath).exists()
    status = "[OK]" if exists else "[FALHOU]"
    print(f"{status} {filepath}")
    return exists

def check_import(module_path: str) -> bool:
    """Verifica se import funciona."""
    try:
        parts = module_path.split('.')
        module = __import__(module_path)
        for part in parts[1:]:
            module = getattr(module, part)
        print(f"[OK] Import OK: {module_path}")
        return True
    except Exception as e:
        print(f"[FALHOU] Import FALHOU: {module_path} - {e}")
        return False

def check_no_types_conflict() -> bool:
    """Verifica se não há conflito com módulo types."""
    types_dir = Path("examples/copy_creator/types")
    if types_dir.exists():
        print(f"[FALHOU] ERRO: Diretorio 'types/' ainda existe em copy_creator!")
        print(f"   Renomeie para 'models/' para evitar conflito com Python types")
        return False
    print(f"[OK] Sem conflito de diretorio 'types/'")
    return True

def main():
    print("=" * 60)
    print("VERIFICACAO PRE-DEPLOY RAILWAY")
    print("=" * 60)

    all_ok = True

    # 1. Verificar arquivos essenciais
    print("\n[1] Verificando arquivos essenciais...")
    required_files = [
        "Dockerfile",
        "Procfile",
        "railway.json",
        ".dockerignore",
        "pyproject.toml",
        "src/deepagents/model.py",
        "examples/copy_creator/langgraph.json",
        "examples/copy_creator/graph.py",
    ]

    for file in required_files:
        if not check_file_exists(file):
            all_ok = False

    # 2. Verificar se models/ existe (não types/)
    print("\n[2] Verificando estrutura de diretorios...")
    if not check_file_exists("examples/copy_creator/models/__init__.py"):
        all_ok = False
    if not check_file_exists("examples/copy_creator/models/copy_output.py"):
        all_ok = False
    if not check_no_types_conflict():
        all_ok = False

    # 3. Verificar imports
    print("\n[3] Verificando imports...")
    sys.path.insert(0, str(Path.cwd() / "src"))
    sys.path.insert(0, str(Path.cwd()))

    imports_to_check = [
        "deepagents",
        "deepagents.model",
    ]

    for imp in imports_to_check:
        if not check_import(imp):
            all_ok = False

    # 4. Verificar conteúdo do pyproject.toml
    print("\n[4] Verificando pyproject.toml...")
    with open("pyproject.toml", "r") as f:
        content = f.read()

        if '"tests"' in content or "'tests'" in content:
            print("[FALHOU] pyproject.toml ainda tem referencia a 'tests'")
            all_ok = False
        else:
            print("[OK] pyproject.toml sem referencia a 'tests'")

        if "langchain-google-genai" in content:
            print("[OK] Dependencia langchain-google-genai encontrada")
        else:
            print("[FALHOU] Dependencia langchain-google-genai nao encontrada")
            all_ok = False

    # 5. Verificar modelo Gemini
    print("\n[5] Verificando configuracao do modelo...")
    with open("src/deepagents/model.py", "r") as f:
        content = f.read()

        if "ChatGoogleGenerativeAI" in content:
            print("[OK] Modelo Gemini configurado")
        else:
            print("[FALHOU] Modelo Gemini nao encontrado")
            all_ok = False

    # 6. Verificar variáveis de ambiente exemplo
    print("\n[6] Verificando configuracao de ambiente...")
    if check_file_exists("examples/copy_creator/.env.example"):
        with open("examples/copy_creator/.env.example", "r") as f:
            content = f.read()
            if "GOOGLE_API_KEY" in content:
                print("[OK] .env.example tem GOOGLE_API_KEY")
            else:
                print("[AVISO] .env.example nao tem GOOGLE_API_KEY")

    # Resultado final
    print("\n" + "=" * 60)
    if all_ok:
        print("[SUCESSO] TUDO CERTO! Pronto para deploy na Railway!")
        print("\nProximos passos:")
        print("1. git add .")
        print("2. git commit -m 'fix: Railway deploy ready'")
        print("3. git push")
        print("4. Configure GOOGLE_API_KEY na Railway")
        print("5. Deploy!")
        return 0
    else:
        print("[ERRO] VERIFICACAO FALHOU! Corrija os erros acima.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
