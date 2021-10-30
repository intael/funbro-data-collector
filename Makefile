.EXPORT_ALL_VARIABLES:

export APP_CONTAINER=funbro-data-collector
export DATABASE=db

.PHONY: run
run:
	docker-compose run --rm $(APP_CONTAINER) python -m src IMDB_DAILY --datasets ALL
.PHONY: bash
bash:
	docker-compose run --rm $(APP_CONTAINER) bash

.PHONY: build
build:
	docker-compose build  $(APP_CONTAINER)

.PHONY: rebuild_db
rebuild_db:
	docker-compose stop $(DATABASE) && echo "Y" | docker-compose rm $(DATABASE) && docker-compose up $(DATABASE)


.PHONY: up
up:
	docker-compose up

.PHONY: down
down:
	docker-compose down

.PHONY: restart
restart:
	docker-compose down && docker-compose up

# Development:

.PHONY: test
test:
	docker-compose run $(APP_CONTAINER) tox -e test

.PHONY: flake
flake:
	docker-compose run $(APP_CONTAINER) tox -e flake8

.PHONY: mypy
mypy:
	docker-compose run $(APP_CONTAINER) tox -e mypy

.PHONY: tox
tox:
	docker-compose run $(APP_CONTAINER) tox -p all
