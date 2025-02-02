.PHONY: format
format: 
	python -m ruff format

.PHONY: mypy
mypy:
	python -m mypy src/