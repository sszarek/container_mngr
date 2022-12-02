test:
	pytest tests/

lint:
	flake8 src/

type-check:
	mypy src/container_mngr