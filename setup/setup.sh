#!/usr/bin/env bash
# Instalação em Linux/Mac. Rode na raiz do repositório:  bash setup/setup.sh
set -euo pipefail
echo "== Field Shift: instalação =="

command -v python3 >/dev/null || { echo "Instale o Python 3.10+ primeiro."; exit 1; }
python3 --version

[ -d .venv ] || python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip -q
.venv/bin/python -m pip install -r requirements.txt -q

echo; echo "== Testes =="
.venv/bin/python -m pytest -q

echo; echo "Pronto. Para abrir o app:"
echo "  source .venv/bin/activate"
echo "  streamlit run app/streamlit_app.py"

if command -v claude >/dev/null; then
  echo; echo "Claude Code encontrado. Skills e plugins recomendados: veja setup/ferramentas.md"
fi
