.DEFAULT_GOAL := help
ONESHELL:

PWD  = $(shell pwd)


.PHONY: help                                                                                                                                                                                    
help:                                                                                                                                                                                           
	@echo "Control plane for playing around with a cluster hat on a raspi pi."
	@echo ""
	@echo "Valid targets are:"
	@echo "    build            - Build the rpi_locator docker image."
	@echo "    clean            - Attempts to clean up after ourselves."
	@echo "    clean-forced     - Attempts to clean up, but removes the confirmation. Useful for CICD."
	@echo "    docker-lint      - Lints the Dockerfile found int he main directory."
	@echo "    find-raspberries - Looks for and lists all Rapsberry Pis on your local network."
	@echo "    make-hosts       - Creats an ansible compatible hosts file."
	@echo ""

#TAG := $(shell git rev-parse --short HEAD)                                                                                                                                                      

IMAGE_NAME := rpi_locator
DOCKERFILE := ${IMAGE_NAME}/Dockerfile

.PHONY: build
build:
	@docker build \
	  --file ${DOCKERFILE} \
	  --tag ${IMAGE_NAME} \
	  --platform linux/amd64 \
	  ${PWD}

.PHONY: docker-lint
docker-lint:
	@echo "Running hadolint from a dockercontainer directly, please stand-by. "
	docker container run --rm -i hadolint/hadolint hadolint - < ${DOCKERFILE}

.PHONY: clean
clean:
	@echo "Cleaning up..."
	docker volume prune
	docker image prune
	docker system prune

.PHONY: clean-forced
clean-forced:
	@echo "Cleaning up..."
	@echo "Volumes:"
	@docker volume prune -f
	@echo "Images:"
	@docker image prune -f
	@echo "System:"
	@docker system prune -f

#Note, I've chosen on to chain build. This removes alot of output from the screen.
.PHONY: find-raspberries
find-raspberries:
	@docker run \
	  --rm \
	  -v ${PWD}/${IMAGE_NAME}:/${IMAGE_NAME} \
	  --net=host \
	  ${IMAGE_NAME}

make-hosts:
	@docker run \
	  --rm \
	  -v ${PWD}/${IMAGE_NAME}:/${IMAGE_NAME} \
	  --net=host \
	  ${IMAGE_NAME} \
	  --ansible 
