lint:
	black .
	isort .
	flake8 .
	mypy .

up-db:
	docker-compose up -d db
db:
	docker-compose exec db psql -U postgres -d postgres

dev:
	python main.py

migrations:
	alembic revision --autogenerate

migrate:
	alembic upgrade head

downgrade:
	alembic downgrade -1

migrate-docker:
	docker-compose exec api alembic upgrade head


test:
	pytest -v

coverage:
	pytest  --cov=. --cov-report=term-missing --cov-report=html --cov-report=xml

clean:
	find . -name "*.pyc" -exec rm -f {} \;
	find . -name "*.pyo" -exec rm -f {} \;
	find . -name "__pycache__" -exec rm -rf {} \;
	rm -rf htmlcov
