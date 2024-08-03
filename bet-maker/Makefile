install:
	@echo 'Installing dependency...'
	poetry add ${LIB}

remove:
	poetry remove ${LIB}

run:
	poetry run uvicorn app.main:app --host localhost --port 8000 --reload

test-stand:
	docker-compose -f docker-compose.test.yml up -d --build

migrate-create:
	alembic revision --autogenerate -m ${MIGRATION}

migrate-apply:
	alembic upgrade head
