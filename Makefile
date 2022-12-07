test:
	poetry run pytest tests/

lint:
	poetry run flake8 src/

style-check:
	poetry run black src/ --check

type-check:
	poetry run mypy src/container_mngr

publish:
	poetry config pypi-token.pypi ${PYPI_TOKEN}
	poetry build
	poetry publish

run:
	python -m src.container_mngr