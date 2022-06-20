.PHONY: d-run
d-run:
	@COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_COMPOSE_BUILDKIT=1 docker-compose up --build

.PHONY: d-purge
d-purge:
	@COMPOSE_DOCKER_CLI_BUILD=1 DOCKER_COMPOSE_BUILDKIT=1 docker-compose down --volumes --remove-orphans --rmi local
