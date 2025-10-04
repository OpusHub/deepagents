#!/usr/bin/env python3
"""
Servidor alternativo para Copy Creator usando uvicorn diretamente.
Use este se langgraph CLI não funcionar.
"""

import os
import sys
import uvicorn
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

print("=" * 60)
print("COPY CREATOR SERVER - Direct Uvicorn")
print("=" * 60)

# Debug info
print(f"Python: {sys.version}")
print(f"Working dir: {os.getcwd()}")
print(f"PYTHONPATH: {os.environ.get('PYTHONPATH', 'not set')}")
print(f"PORT: {os.environ.get('PORT', '8000')}")

if os.environ.get('GOOGLE_API_KEY'):
    print(f"GOOGLE_API_KEY: {os.environ['GOOGLE_API_KEY'][:10]}***")
else:
    print("WARNING: GOOGLE_API_KEY not set!")

print("=" * 60)

# Import graph
try:
    from examples.copy_creator.graph import graph
    print("✓ Graph imported successfully")
    print(f"Graph type: {type(graph)}")
except Exception as e:
    print(f"✗ Failed to import graph: {e}")
    sys.exit(1)

# Get port
port = int(os.environ.get("PORT", 8000))

# Create simple FastAPI app wrapping the graph
try:
    from fastapi import FastAPI
    from langserve import add_routes

    app = FastAPI(
        title="Copy Creator Agent",
        description="LangGraph agent for creating marketing copies",
        version="1.0.0"
    )

    # Add graph routes
    add_routes(app, graph, path="/copy_creator")

    # Health check
    @app.get("/info")
    async def info():
        return {
            "name": "copy_creator",
            "status": "running",
            "port": port
        }

    print(f"✓ FastAPI app created")
    print(f"Starting server on 0.0.0.0:{port}")
    print("=" * 60)

    # Run server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )

except Exception as e:
    print(f"✗ Failed to create/run server: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
