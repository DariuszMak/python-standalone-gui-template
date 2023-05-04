# Python Standalone GUI template

## Dependencies

- Python 3.10.10
- Docker


### Running Docker container service

Basic usage:

```
docker-compose up -d --build
docker-compose run app
```

## Another useful Docker commands

Regular usage:
```
docker compose up
```

or in detached mode:

```
docker compose up -d
```

Build images before starting containers and force recreate containers even if their configuration and image haven't changed:
```
docker compose up --build --force-recreate --always-recreate-deps
```

After the job is done (optionally)
```
docker compose down
```