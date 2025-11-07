# Name of the Docker image
IMAGE_NAME=fastapi-app

# Docker-related commands
DOCKER=docker
DOCKER_COMPOSE=docker-compose

# Port on the host machine
HOST_PORT=8000
CONTAINER_PORT=8000

# Build the Docker image
build:
	@echo "Building the Docker image..."
	$(DOCKER) build -t $(IMAGE_NAME) .

# Run the FastAPI container in detached mode
run:
	@echo "Running the Docker container..."
	$(DOCKER) run -d -p $(HOST_PORT):$(CONTAINER_PORT) $(IMAGE_NAME)

# Stop the running Docker container
stop:
	@echo "Stopping the Docker container..."
	$(DOCKER) ps -q --filter "ancestor=$(IMAGE_NAME)" | xargs $(DOCKER) stop

# Remove the stopped Docker container
remove:
	@echo "Removing the Docker container..."
	$(DOCKER) ps -aq --filter "ancestor=$(IMAGE_NAME)" | xargs $(DOCKER) rm

# Remove the Docker image
remove-image:
	@echo "Removing the Docker image..."
	$(DOCKER) rmi $(IMAGE_NAME)

# Clean: Stop, remove container, and remove the image
clean: stop remove remove-image

# Run the application using Docker Compose (optional if you use Docker Compose)
up:
	@echo "Starting application using Docker Compose..."
	$(DOCKER_COMPOSE) up --build

# Stop Docker Compose containers
down:
	@echo "Stopping application using Docker Compose..."
	$(DOCKER_COMPOSE) down

# Rebuild the Docker image and run the container
rebuild: clean build run

# Display the status of the containers
status:
	@echo "Getting the status of running containers..."
	$(DOCKER) ps
