.PHONY: list test

SERVICE_DOCKERFILE = Dockerfile_service
SERVICE_IMAGE = cdn_image
SERVICE_CONTAINER = cdn_container

UNITTEST_DOCKERFILE = Dockerfile_unittest
UNITTEST_IMAGE = cdn_unittest_image
UNITTEST_CONTAINER = cdn_unittest_container

FUNC_DOCKERFILE = Dockerfile_func
FUNC_IMAGE = cdn_func_image
FUNC_CONTAINER = cdn_func_container
FUNC_COMPOSE = docker-compose.func.yml


list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

volume_up:
	docker volume create cdn_main
	docker volume create cdn_1
	docker volume create cdn_2

volume_down:
	docker volume rm --force cdn_main
	docker volume rm --force cdn_1
	docker volume rm --force cdn_2

build:
	docker build -f $(SERVICE_DOCKERFILE) -t $(SERVICE_IMAGE) .

debug:
	make build
	make volume_up
	docker run --rm --net=host \
	--mount source=cdn_main,destination=/app/data/cdn_main \
	--mount source=cdn_1,destination=/app/data/cdn_1 \
	--mount source=cdn_2,destination=/app/data/cdn_2 \
	-p 8080:8080 \
	--name $(SERVICE_CONTAINER) \
	$(SERVICE_IMAGE)
	make volume_down

run:
	make volume_up
	make build
	docker run --rm --net=host -d \
	--mount source=cdn_main,destination=/app/data/cdn_main \
	--mount source=cdn_1,destination=/app/data/cdn_1 \
	--mount source=cdn_2,destination=/app/data/cdn_2 \
	-p 8080:8080 \
	--name $(SERVICE_CONTAINER) \
	$(SERVICE_IMAGE)

stop:
	docker stop $(SERVICE_CONTAINER)
	make volume_down

test:
	make volume_up
	docker build -f $(UNITTEST_DOCKERFILE) -t $(UNITTEST_IMAGE) .
	docker run --rm --net=host \
	--mount source=cdn_main,destination=/app/service/data/cdn_main \
	--mount source=cdn_1,destination=/app/service/data/cdn_1 \
	--mount source=cdn_2,destination=/app/service/data/cdn_2 \
	--name $(UNITTEST_CONTAINER) \
	$(UNITTEST_IMAGE)
	make volume_down

compose_debug:
	make volume_up
	make build
	docker-compose -f $(FUNC_COMPOSE) up
	make volume_down


func:
	make volume_up
	make build
	-docker-compose -f $(FUNC_COMPOSE) rm -fs
	docker-compose -f $(FUNC_COMPOSE) up -d
	sleep 3
	docker build -f $(FUNC_DOCKERFILE) -t $(FUNC_IMAGE) .
	docker run --rm --net=host \
	--mount source=cdn_main,destination=/app/data/cdn_main \
	--mount source=cdn_1,destination=/app/data/cdn_1 \
	--mount source=cdn_2,destination=/app/data/cdn_2 \
	--name $(FUNC_CONTAINER) \
	$(FUNC_IMAGE)

	docker-compose -f $(FUNC_COMPOSE) rm -fs
	make volume_down