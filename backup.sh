#!/bin/bash
# Ativa o venv e executa o script de backup
source /root/postgres_backup/venv/bin/activate
/root/postgres_backup/venv/bin/python /root/postgres_backup/postgres_backup.py
