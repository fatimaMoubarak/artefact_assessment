# Makefile Reference

This Makefile streamlines Docker workflows for the FastAPI ABSA service. Every target assumes Docker/ Docker Compose are installed and that you run the commands from the project root:

```bash
make <target>
```

## Targets
- `build`: Builds the image (`fastapi-app`) from the current Dockerfile.
- `run`: Runs the image in detached mode and maps `HOST_PORT` (default `8000`) to the container port.
- `stop`: Stops containers created from the `fastapi-app` image.
- `remove`: Removes stopped containers created from the image.
- `remove-image`: Deletes the `fastapi-app` image.
- `clean`: Convenience alias that runs `stop`, `remove`, and `remove-image` sequentially.
- `up`: Uses Docker Compose to build and start services (requires `docker-compose.yml`).
- `down`: Stops Compose services defined in the compose file.
- `rebuild`: Executes `clean`, then rebuilds and reruns the container (`build` + `run`).
- `status`: Shows currently running Docker containers (`docker ps`).

## Customizing Ports or Image Name
Edit the variables at the top of the Makefile:

```makefile
IMAGE_NAME=fastapi-app
HOST_PORT=8000
CONTAINER_PORT=8000
```

Changing `HOST_PORT` lets you expose the API on a different local port, while `IMAGE_NAME` isolates multiple builds on the same machine.

## Typical Workflow
1. `make build`
2. `make run`
3. Iterate on your code; restart with `make stop` and `make run`, or rebuild via `make rebuild`.
4. When finished, clean up artifacts using `make clean`.

## Troubleshooting
- If `make stop` prints “xargs: command not found” on Windows, run the equivalent Docker commands manually or install a POSIX-compatible shell (e.g., Git Bash).
- Ensure Docker daemon is running before invoking any target; otherwise `docker build`/`docker run` will fail.
