PROJECT_NAME=order_service
COMPOSE_PROD=docker compose -f docker-compose.yml -p $(PROJECT_NAME)

build_prod:
	$(COMPOSE_PROD) build postgres
	$(COMPOSE_PROD) build web
	$(COMPOSE_PROD) build celery_worker
	$(COMPOSE_PROD) build redis
	$(COMPOSE_PROD) build rabbitmq


check_web:
	@if docker ps --filter "name=orders_app" --format "{{.Names}}" | grep -q "^orders_app$$"; then \
		echo "The container 'web' is running."; \
	else \
		echo "The container 'web' is not running. Run \"make run_prod\" first"; \
		exit 1; \
	fi

migrate: check_web ## Creates a new migration with a given name or default 'update'
	@name=$(if $(filter-out $@,$(MAKECMDGOALS)), $(filter-out $@,$(MAKECMDGOALS)), "update"); \
	docker exec -it orders_app /app/.venv/bin/alembic -c alembic.ini revision -m "$$name" --autogenerate

upgrade: check_web ## Creates a new migration with a given name or default 'update'
	docker exec -it orders_app /app/.venv/bin/alembic -c alembic.ini upgrade head


run_prod: build_prod
	$(COMPOSE_PROD) up -d

down: ## Stops all running containers
	docker compose down

clean_db: ## Removes the database container and its associated volume
	@docker compose stop db || true
	@docker compose rm -f db || true
	@docker volume rm $$(docker volume ls -q --filter name=${PWD##*/}_postgres_data) || true

clean_all: clean_db ## Completely removes all containers, volumes, images, and orphaned services
	@docker compose down -v --rmi all --remove-orphans || true
	@docker volume prune -f || true

logs: ## Displays logs for the specified service
	docker compose logs -f $(filter-out $@,$(MAKECMDGOALS))

test: check_web ## Run tests
	docker exec -it orders_app pytest

help: ## Lists all available Makefile commands with their descriptions
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

%:
	@: