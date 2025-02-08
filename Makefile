export GOOGLE_APPLICATION_CREDENTIALS=credentials.json

.PHONY: format
format: 
	python -m ruff check --select I --fix
	python -m ruff format

.PHONY: mypy
mypy:
	python -m mypy src/

.PHONY: test
test:
	python -m pytest

.PHONY: local
local:
	python -m src.main
