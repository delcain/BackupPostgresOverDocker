# Postgres Backup

Este projeto contém scripts para realizar backups automatizados de bancos de dados PostgreSQL executando em containers Docker.
Os scripts localizam automaticamente todos os containers Docker rodando PostgreSQL e realizam o backup de todos os bancos possíveis.

## Arquivos

- `postgres_backup.py`: Script principal em Python para realizar o backup dos bancos de dados PostgreSQL em containers Docker.
- `backup.sh`: Script shell para automatizar o processo de backup em ambientes Linux/macOS.
- `requirements.txt`: Lista de dependências Python necessárias para executar o script.

## Como usar

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

### 2. Execute o script de backup

O script irá localizar automaticamente todos os containers Docker rodando PostgreSQL e realizar o backup de todos os bancos de dados disponíveis.

#### Usando Python:

```bash
python postgres_backup.py
```

#### Usando Shell Script:

```bash
sh backup.sh
```

## Personalização

- Edite o script `postgres_backup.py` para alterar o diretório de destino do backup ou adicionar funcionalidades extras.
- O script pode ser agendado via cron no Linux para backups automáticos.

## Exemplo de agendamento (Linux)

Utilize o cron para agendar execuções automáticas do script:

```bash
0 2 * * * /usr/bin/python /caminho/para/postgres_backup.py
```

## Licença

Este projeto é distribuído sob a licença MIT.

---

> Feito com ❤️ para facilitar backups automáticos e seguros de bancos PostgreSQL em containers Docker.
