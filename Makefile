# Dont use for now
# setup:
# 	@echo "Activating virtual enviroment..."
# 	. .enviroment/bin/activate

run:
	python3 runserver.py

lint:
	ruff check

lint-fix:
	ruff check --fix

formatt:
	ruff format

# #!/bin/bash
#
# 	@echo "Activating virtual environment..."
# 	source .enviroment/bin/activate
#
# setup-2:
# 	\
# 		source .enviroment/bin/activate; \
