PYTHON_VERSION := $(shell cat .python-version)
RUN = . .venv/bin/activate;

include .env

ENV_CONFIGS_PATH = app/config/envs
ENV_FILE = $(PWD)/$(ENV_CONFIGS_PATH)/$(APP_VERSION).env

include $(ENV_FILE)

pwd:
	echo $(APP_VERSION)
	echo $(ENV_FILE)

init:
	uv venv -nv -p $(PYTHON_VERSION) .venv

install:
	$(RUN) uv sync

venv: init install

clean:
	rm -rf .venv

create_db:
	docker exec -it postgres createdb -U $(DB_USER) -h $(DB_HOST) -p $(DB_PORT) $(DB_NAME)

drop_db:
	-docker exec -it postgres dropdb $(DB_NAME) -U $(DB_USER) && \
	echo 'DB $(DB_NAME) dropped successfully'

run_migrations:
	export $(APP_VERSION) && \
	$(RUN) alembic upgrade head

lint:
	$(RUN) ruff format
	$(RUN) ruff check --fix

run_app:
	export APP_VERSION=dev && docker compose up --build
