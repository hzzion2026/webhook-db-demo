.PHONY: run test clean docker-up docker-down

run:
	uvicorn app:app --reload --host 0.0.0.0 --port 8000

test:
	pytest tests/ -v --asyncio-mode=auto

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down

clean:
	find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name *.pyc -delete
