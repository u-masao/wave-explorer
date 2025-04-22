run:
	uv run python -m src.main
lint:
	uv run ruff format src
	uv run ruff check src
