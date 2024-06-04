.PHONY: format start start_db stop test build start_prod stop_prod

include .env
export $(shell sed 's/=.*//' .env)

format:
	hatch fmt -f
	hatch fmt

start_db:
	docker-compose --profile db up -d

start: start_db
	hatch run bot

stop:
	docker-compose down -v

test: start_db
	hatch run pytest

build:
	docker build -t clown_bot:latest .

start_prod:
	docker-compose --profile prod up -d

stop_prod:
	docker-compose --profile prod down -v
