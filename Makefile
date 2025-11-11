.PHONY: all setup-python lint-python lint-shell lint-yaml fix-python test-python

all:

setup: setup-python

setup-python:
	python3 -m virtualenv .venv
	.venv/bin/pip install litellm boto3 azure-storage-blob tenacity=8.5.0
	.venv/bin/pip install ruff pyright yamllint pre-commit

lint: lint-python lint-shell lint-yaml

lint-python:
	.venv/bin/ruff check ./
	.venv/bin/ruff format --check ./
	.venv/bin/pyright ./

lint-shell:
	find . -name "*.sh" -not -path "./.venv/*"

lint-yaml:
	.venv/bin/yamllint ./

fix: fix-python

fix-python:
	.venv/bin/ruff check --fix ./
	.venv/bin/ruff format ./

test: test-python

test-python:
	.venv/bin/python -m unittest discover ./
