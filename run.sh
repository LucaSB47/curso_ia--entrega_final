#!/usr/bin/env bash
set -e

echo "=== Iniciando Intelligence Hardware Support System ==="

if [ -d "venv/Scripts" ]; then
    source venv/Scripts/activate
elif [ -d "venv/bin" ]; then
    source venv/bin/activate
fi

python -m uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload