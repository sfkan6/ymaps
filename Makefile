.DEFAULT_GOAL := help
.ONESHELL:
.PHONY: changelog coverage deps help lint push test venv


coverage:	## Run tests with coverage
	coverage erase
	coverage run --include=ymaps/* -m pytest -ra
	coverage report -m

check:	## Lint and static-check
	flake8 --max-line-length 90 ymaps
	mypy ymaps

deps:	## Install dependencies
	python -m pip install -r requirements-test.txt black

test:	## Run tests
	pytest -ra

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
