default: lint

lint:
    uv run --with ruff ruff check src

typecheck:
    uv run --group dev mypy src

docs:
    uv run --group docs --extra server --extra client mkdocs serve
