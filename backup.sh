#!/bin/bash
# Ativa o venv e executa o script de backup, usando caminhos relativos

# Caminho do diretório onde este script está
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Ativa o ambiente virtual
source "$SCRIPT_DIR/venv/bin/activate"

# Executa o script Python
python "$SCRIPT_DIR/postgres_backup.py"

