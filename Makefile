.PHONY: help dev format test

help:
	@echo "This project uses Poetry to manage its dependencies. Make sure you have poetry installed before running any make command"
	@echo "The following make targets are available:"
	@echo "	 dev 	install all deps for dev env"
	@echo "  format	formats all files with black"
	@echo "	 test	run all tests with coverage"

dev:
	poetry shell
	poetry install


format:
	black --line-length 75 .
	flake8 moapi tests
	git status


test:
	black --line-length 75 .
	flake8 moapi tests
	pytest -vv --cov-report term-missing --cov=moapi tests/
	@echo "!!!!  TESTING COMPLETE  !!!!!"

deploy:
	poetry build
	poetry publish
