import docker
import subprocess
import os
import gzip
import shutil
from datetime import datetime, timedelta

# Configurações
backup_dir = "/mnt/storage/backups"
days_to_keep = 30  # quantos dias manter os backups
os.makedirs(backup_dir, exist_ok=True)

client = docker.from_env()

def compress_file(filepath):
    """Compacta um arquivo .sql em .sql.gz"""
    gz_path = filepath + ".gz"
    with open(filepath, "rb") as f_in, gzip.open(gz_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)
    os.remove(filepath)  # remove o original .sql
    return gz_path

def rotate_backups():
    """Remove backups mais antigos que days_to_keep"""
    cutoff = datetime.now() - timedelta(days=days_to_keep)
    for filename in os.listdir(backup_dir):
        path = os.path.join(backup_dir, filename)
        if os.path.isfile(path):
            mtime = datetime.fromtimestamp(os.path.getmtime(path))
            if mtime < cutoff:
                os.remove(path)
                print(f"🗑️  Backup antigo removido: {path}")

for container in client.containers.list():
    try:
        image = container.image.tags[0] if container.image.tags else ""
        if "postgres" not in image.lower():
            continue  # ignora containers que não são postgres

        # Extrai variáveis
        envs = container.attrs['Config']['Env']
        db_user = next((e.split("=")[1] for e in envs if e.startswith("POSTGRES_USER=")), "postgres")
        db_name = next((e.split("=")[1] for e in envs if e.startswith("POSTGRES_DB=")), None)

        if db_name:
            # Backup de apenas um banco
            dump_file = os.path.join(
                backup_dir,
                f"{container.name}_{db_name}_{datetime.now():%Y%m%d%H%M}.sql"
            )
            cmd = ["docker", "exec", container.id[:12], "pg_dump", "-U", db_user, db_name]
            with open(dump_file, "w") as f:
                subprocess.run(cmd, stdout=f, check=True)

            gz_file = compress_file(dump_file)
            print(f"✅ Backup de {db_name} no container {container.name} (user={db_user}) salvo em {gz_file}")

        else:
            # Lista todos os bancos
            list_cmd = [
                "docker", "exec", container.id[:12],
                "psql", "-U", db_user, "-t", "-c", "SELECT datname FROM pg_database WHERE datistemplate = false;"
            ]
            result = subprocess.run(list_cmd, capture_output=True, text=True, check=True)
            databases = [db.strip() for db in result.stdout.splitlines() if db.strip()]

            for db in databases:
                dump_file = os.path.join(
                    backup_dir,
                    f"{container.name}_{db}_{datetime.now():%Y%m%d%H%M}.sql"
                )
                cmd = ["docker", "exec", container.id[:12], "pg_dump", "-U", db_user, db]
                with open(dump_file, "w") as f:
                    subprocess.run(cmd, stdout=f, check=True)

                gz_file = compress_file(dump_file)
                print(f"✅ Backup de {db} no container {container.name} (user={db_user}) salvo em {gz_file}")

    except Exception as e:
        print(f"❌ Erro no container {container.name}: {e}")

# Rotação automática
rotate_backups()

