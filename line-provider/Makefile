install:
	@echo 'Installing dependency...'
	poetry add ${LIB}

remove:
	poetry remove ${LIB}

run:
	poetry run uvicorn app.main:app --host localhost --port 8001 --reload

test-stand:
	docker-compose -f docker-compose.test.yml up -d --build
