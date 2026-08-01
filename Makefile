up:
	docker compose \
	-f docker-compose.yml \
	-f docker-compose.infrastructure.yml up -d

down:
	docker compose down

logs:
	docker compose logs -f

ps:
	docker ps

clean:
	docker compose down -v