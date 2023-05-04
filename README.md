# Python Standalone GUI template

## Dependencies

- Python 3.9.x
- Docker


### Running the container service

Regular usage:
```
docker compose up
```

Build images before starting containers and force recreate containers even if their configuration and image haven't changed:
```
docker compose up --build --force-recreate --always-recreate-deps
```

After the job is done (optionally)
```
docker compose down
```