.EXPORT_ALL_VARIABLES:

export CONTAINER=funbro-data-collector
export DATABASE=db

.PHONY: run
run:
	docker exec $(CONTAINER) python main.py --num_cores 4 autoscout --task AUTOSCOUT_CRAWLER --countries ALL --body_colors ALL --makes ALL --bodies ALL --freg_from 2014 --min_doors ALL

.PHONY: bash
bash:
	docker-compose run $(CONTAINER) bash

.PHONY: build
build:
	docker-compose up --build

.PHONY: database
database:
	docker exec -ti $(DATABASE) mysql -u root -passwd -D business_intelligence

.PHONY: rebuild_db
rebuild_db:
	docker-compose rm db && docker-compose stop db && docker-compose up db

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
