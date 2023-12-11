docker compose -f docker-compose.yml -f docker-compose.test.yml -f docker-compose.test.watch.yml -f docker-compose.cli.yml up --build -d
docker attach horizon-app
docker compose -f docker-compose.yml -f docker-compose.test.yml -f docker-compose.test.watch.yml -f docker-compose.cli.yml down