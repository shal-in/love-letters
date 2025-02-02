.PHONY: format
format: 
	python -m ruff format

.PHONY: mypy
mypy:
	python -m mypy src/

.PHONY: test
test:
	python -m pytest