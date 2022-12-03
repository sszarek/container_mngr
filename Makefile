test:
	poetry run pytest tests/

lint:
	poetry run flake8 src/

style-check:
	poetry run black src/ --check

type-check:
	poetry run mypy src/container_mngr