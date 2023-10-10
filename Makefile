build:
	docker-compose build

up:
	docker-compose up app

tests:
	docker-compose run app . /opt/venv/bin/activate || pip install -r requirements_dev.txt && pytest . --cov=.

logs:
	docker-compose logs app | tail -100

down:
	docker-compose down

all: down build up tests
