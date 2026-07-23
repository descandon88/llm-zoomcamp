


run:
	uv run python assistant.py

chat:
	docker-compose -f ../docker-compose.yml up -d --build module-05

network:
    docker network create monitoring

init-db:
    docker compose exec module-05 python db_init.py

reset-db:
    docker compose exec module-05 python db_init.py --drop

query:
	docker compose exec module-05 python db_query.py