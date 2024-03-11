.PHONY: lint format dependencies env start

include .env
export $(shell sed 's/=.*//' .env)

PYTHONPATH := export PYTHONPATH=$(shell pwd)/src


lint:
	./bin/lint.sh

format:
	./bin/format.sh

dependencies:
	poetry lock
	poetry export -f requirements.txt -f requirements.txt -o requirements.txt --without-hashes

env:
	poetry shell
	poetry install --with dev --all-extras

start:
	(export PYTHONPATH=$(PYTHONPATH) ; poetry shell)
	(export PYTHONPATH=$(PYTHONPATH) ; python src/clown_bot/main.py)
