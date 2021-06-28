.EXPORT_ALL_VARIABLES:

export CONTAINER=funbro-data-collector
export DATABASE=db

.PHONY: run
run:
	docker-compose run --rm $(CONTAINER) python -m src IMDB_DAILY --datasets TITLE_RATINGS
	docker-compose stop $(CONTAINER)
.PHONY: bash
bash:
	docker-compose run --rm $(CONTAINER) bash

.PHONY: build
build:
	docker-compose build --no-cache $(CONTAINER)

.PHONY: database
database:
	docker exec -ti $(DATABASE) PGPASSWORD=test psql -h 172.28.1.2 -U test_user -c '\q'

.PHONY: rebuild_db
rebuild_db:
	docker-compose stop $(DATABASE) &&  echo "Y" | docker-compose rm $(DATABASE) && docker-compose up $(DATABASE)

.PHONY: test
test:
	docker-compose run $(CONTAINER) pytest

.PHONY: mypy
mypy:
	docker-compose run $(CONTAINER) mypy src

.PHONY: up
up:
	docker-compose up

.PHONY: down
down:
	docker-compose down

.PHONY: restart
restart:
	docker-compose down && docker-compose up
