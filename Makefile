.PHONY: install run test lint clean

install:
	pip install -r requirements.txt && pip install -e .

run:
	python -m src.processing.run \
		--input data/raw/sample.csv \
		--output data/processed/sample_clean.csv

test:
	pytest tests/ -v

lint:
	ruff check src/ tests/ || true

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -rf .pytest_cache htmlcov .coverage
