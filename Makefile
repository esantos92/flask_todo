# ========= Config =========
SHELL := /bin/bash
export PYTHONDONTWRITEBYTECODE=1
export FLASK_APP := app:create_app
export PYTHONPATH := $(PWD)

# Carrega .env ao chamar targets que rodam app
dotenv = set -a; source .env; set +a;
# Ativa ambiente virtual
venv = source .venv/bin/activate;

# ========= Convenções =========
.PHONY: help env up down logs psql redis-cli run worker beat \
        db-init db-migrate db-upgrade db-downgrade db-stamp db-revision \
        lint fmt typecheck test seed clean

help:
	@echo "Targets úteis:"
	@echo "  env           - ativa venv (dica de uso)"
	@echo "  up / down     - sobe/derruba Postgres e Redis (docker compose)"
	@echo "  run           - roda a API Flask"
	@echo "  worker / beat - Celery worker e beat"
	@echo "  db-init       - cria diretório de migrações"
	@echo "  db-migrate    - autogera migração (use VAR m='msg')"
	@echo "  db-upgrade    - aplica migrações"
	@echo "  db-downgrade  - reverte 1 versão"
	@echo "  db-stamp      - marca head sem alterar schema (use com cuidado)"
	@echo "  db-revision   - cria revisão vazia manual (use VAR m='msg')"
	@echo "  lint / fmt    - ruff + black"
	@echo "  typecheck     - mypy"
	@echo "  test          - pytest"
	@echo "  seed          - popula dados de exemplo (se existir comando)"
	@echo "  logs          - logs do compose"
	@echo "  psql          - abre psql no container"
	@echo "  redis-cli     - abre redis-cli no container"

env:
	@echo "Use: source .venv/bin/activate"

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

psql:
	docker compose exec -it db psql -U app -d app_db

redis-cli:
	docker compose exec -it redis redis-cli

run:
	@$(venv) $(dotenv) flask run --host=0.0.0.0 --port=5000 --debug

worker:
	@$(venv) $(dotenv) celery -A app.tasks.celery_app.celery worker --loglevel=INFO

beat:
	@$(venv) $(dotenv) celery -A app.tasks.celery_app.celery beat --loglevel=INFO

db-init:
	@$(venv) $(dotenv) flask db init

# use: make db-migrate m="mensagem da migracao"
db-migrate:
	@$(venv) $(dotenv) flask db migrate -m "$(m)"

db-upgrade:
	@$(venv) $(dotenv) flask db upgrade

db-downgrade:
	@$(venv) $(dotenv) flask db downgrade

# marca o banco como estando no 'head' sem executar scripts (cautela)
db-stamp:
	@$(venv) $(dotenv) flask db stamp head

# cria revisão vazia para editar manualmente
# use: make db-revision m="ajuste manual"
db-revision:
	@$(venv) $(dotenv) alembic revision -m "$(m)"

lint:
	$(venv) ruff check app

fmt:
	$(venv) black app

typecheck:
	$(venv) mypy app --ignore-missing-imports

test:
	$(venv) pytest -q

seed:
	@echo "Implemente um comando de seed (ex: Flask CLI custom)."

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} \; || true
	rm -rf .pytest_cache .mypy_cache
