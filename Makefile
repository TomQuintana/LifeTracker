run:
	python3 runserver.py

lint:
	ruff check

lint-fix:
	ruff check --fix

formatt:
	ruff format
