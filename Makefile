prod:
	docker compose -f docker-compose.yml up --build

test:
	docker compose -f docker-compose.yml -f docker-compose.test.yml up --build --exit-code-from app

test-watch:
	docker compose -f docker-compose.yml -f docker-compose.test.yml -f docker-compose.test.watch.yml up --build --no-attach db --no-attach pgadmin

repl:
	docker compose -f docker-compose.yml -f docker-compose.test.yml -f docker-compose.test.watch.yml -f docker-compose.cli.yml up --build -d
	docker attach horizon-app