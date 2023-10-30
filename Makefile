.DEFAULT_GOAL := help
.ONESHELL:
.PHONY:


deps:	## Install development dependencies
	python -m pip install -r requirements-dev.txt

lint:	## Lint and static-check
	flake8 --max-line-length 100 ymaps
	mypy ymaps

format: ## Format the code
	black ymaps tests

test:	## Run tests
	pytest -ra

coverage:	## Run tests with coverage
	coverage erase
	coverage run --include=ymaps/* -m pytest -ra
	coverage report -m

tox:	## Run tox
	tox

help:	## Show help message
	@IFS=$$'\n' ; \
	help_lines=(`fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##/:/'`); \
	printf "%s\n\n" "Usage: make [task]"; \
	printf "%-20s %s\n" "task" "help" ; \
	printf "%-20s %s\n" "------" "----" ; \
	for help_line in $${help_lines[@]}; do \
		IFS=$$':' ; \
		help_split=($$help_line) ; \
		help_command=`echo $${help_split[0]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		help_info=`echo $${help_split[2]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		printf '\033[36m'; \
		printf "%-20s %s" $$help_command ; \
		printf '\033[0m'; \
		printf "%s\n" $$help_info; \
	done
