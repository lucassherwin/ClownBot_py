.PHONY: format start start_db stop test

include .env
export $(shell sed 's/=.*//' .env)

format:
	hatch fmt -f
	hatch fmt

start_db:
	docker-compose up -d

start: start_db
	hatch run bot

stop:
	docker-compose down -v

test: start_db
	hatch run pytest
