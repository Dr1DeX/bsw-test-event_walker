install:
	@echo 'Installing dependency...'
	poetry add ${LIB}

migrate-create:
	alembic revision --autogenerate -m ${MIGRATION}

migrate-apply:
	alembic upgrade head