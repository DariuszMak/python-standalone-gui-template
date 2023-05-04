# Python Standalone GUI template

## Dependencies

- Python 3.9.x
- Docker


### Running the container service

To specify run containers:

```
docker-compose up -d --build
docker-compose run app
```

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