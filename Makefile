.PHONY: format
format: 
	python -m ruff format

.PHONY: mypy
mypy:
	python -m mypy src/

.PHONY: test
test:
	python -m pytest

.PHONY: local
local:
	python src/app.py