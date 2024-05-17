VERSION_FILE := version.txt
CURRENT_VERSION := $(shell cat $(VERSION_FILE))

.PHONY: clean build run logs

include .env

default: help

help:
	@echo "USAGE:"
	@echo "  start:                  starts backend and database"
	@echo "  postgres:               starts database"
	@echo "  stop:                   stops backend and database"
	@echo "  build:                  builds backend and database"
	@echo "  build-postgres:         builds database"
	@echo "  logs:                   show logs for services"
	@echo "  test:                   runs tests"
	@echo "  flake8:                 runs flake8"
	@echo "  clean:                  stops and deletes all services including volumes"
	@echo "  test-database:          creates test database"
	@echo "  import-dummy:           imports dummy data"
	@echo "  import-local-corpus:    imports local corpus"
	@echo "  import-remote-corpus:   imports remote corpus"
	@echo "  list-remote-corpora:    lists remote corpora"

start:
	docker compose up -d

postgres:
	docker compose up db -d

stop:
	docker compose stop

build:
	docker compose build

down:
	docker compose down -v

logs:
	docker compose logs -f

test:
	docker compose exec backend tox -e pytest

flake8:
	docker compose exec backend bash -c 'if grep -q "^\[testenv:flake8\]" ./tox.ini; then tox -e flake8; else echo "No flake8 found, skipping!"; fi'

clean:
	docker compose down --volumes

create-database:
	docker compose exec backend ./scripts/dbtool.py --create-database --force

test-database:
	docker compose exec db sh -c 'psql -U ${DB_USER} -c "CREATE DATABASE ${ORBIS_DB_TEST_NAME}"' 

import-dummy:
	docker compose exec backend ./scripts/dbtool.py --create-database --force --add-dummy-data

import-local-corpus:
	docker compose exec backend ./scripts/importer.py local KORE50.ttl KORE50-version1.0

import-remote-corpus:
	docker compose exec backend ./scripts/importer.py remote N3-Reuters-128 N3-Reuters-128-version1

list-remote-corpora:
	docker compose exec backend ./scripts/importer.py list-remote

release_major_version:
	$(eval MAJOR_VERSION := $(word 1, $(subst ., ,$(CURRENT_VERSION))))
	$(eval NEW_MAJOR_VERSION := $(shell echo $$(($(MAJOR_VERSION)+1))))
	$(eval NEW_VERSION := $(NEW_MAJOR_VERSION).0.0)
	@echo "Current version: $(CURRENT_VERSION)"
	@echo "New version: $(NEW_VERSION)"
	echo $(NEW_VERSION) > $(VERSION_FILE)
	git add version.txt
	git commit -m "Major Release $(NEW_VERSION)"
	git tag $(NEW_VERSION)
	echo "INFO: Please git push the new major version manually"

release_minor_version:
	$(eval MINOR_VERSION := $(word 2, $(subst ., ,$(CURRENT_VERSION))))
	$(eval NEW_MINOR_VERSION := $(shell echo $$(($(MINOR_VERSION)+1))))
	$(eval NEW_VERSION := $(word 1, $(subst ., ,$(CURRENT_VERSION))).$(NEW_MINOR_VERSION).0)
	@echo "Current version: $(CURRENT_VERSION)"
	@echo "New version: $(NEW_VERSION)"
	echo $(NEW_VERSION) > $(VERSION_FILE)
	git add version.txt
	git commit -m "Minor Release $(NEW_VERSION)"
	git tag $(NEW_VERSION)
	git push --tags
	echo "INFO: Please git push the new minor version manually"

release_patch_version:
	$(eval PATCH_VERSION := $(word 3, $(subst ., ,$(CURRENT_VERSION))))
	$(eval NEW_PATCH_VERSION := $(shell echo $$(($(PATCH_VERSION)+1))))
	$(eval NEW_VERSION := $(word 1, $(subst ., ,$(CURRENT_VERSION))).$(word 2, $(subst ., ,$(CURRENT_VERSION))).$(NEW_PATCH_VERSION))
	@echo "Current version: $(CURRENT_VERSION)"
	@echo "New version: $(NEW_VERSION)"
	echo $(NEW_VERSION) > $(VERSION_FILE)
	git add version.txt
	git commit -m "Patch Release $(NEW_VERSION)"
	git tag $(NEW_VERSION)
	git push --tags
	echo "INFO: Please git push the new patch version manually"