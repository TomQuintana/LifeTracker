run:
	poetry run python runserver.py

lint:
	ruff check

lint-fix:
	ruff check --fix

formatt:
	ruff format
