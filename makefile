.PHONY: clean build run logs

include .env

default: help

help:
	@echo "USAGE:"
	@echo "  start:                  starts all services"
	@echo "  stop:                   stops all services including volumes"
	@echo "  build:                  builds all services"
	@echo "  logs:                   show logs for services"
	@echo "  clean:                  clean up workspace"
	@echo "  test-database:          creates test database"
	@echo "  import-dummy:           imports dummy data"
	@echo "  import-local-corpus:    imports local corpus"
	@echo "  import-remote-corpus:   imports remote corpus"

start:
	docker compose up -d

stop:
	docker compose stop

build:
	docker compose build

logs:
	docker compose logs

clean:
	docker compose down --volumes

test-database:
	docker compose exec db sh -c 'psql -U ${DB_USER} -c "CREATE DATABASE ${ORBIS_DB_TEST_NAME}"' 

import-dummy:
	docker compose exec backend ./scripts/dbtool.py --create-database --force --add-dummy-data

import-local-corpus:
	docker compose exec backend ./scripts/importer.py local KORE50.ttl KORE50-version1.0

import-remote-corpus:
	docker compose exec backend ./scripts/importer.py local KORE50.ttl KORE50-version1.0

