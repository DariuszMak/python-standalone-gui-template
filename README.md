# Python Standalone GUI template

## Dependencies

- Python 3.10.10
- Docker

### Local configuration:
```
python -m pip install virtualenv
python -m virtualenv venv
```

On Unix or MacOS, using the bash shell: `source venv/bin/activate`

On Unix or MacOS, using the csh shell: `source venv/bin/activate.csh`

On Unix or MacOS, using the fish shell: `source venv/bin/activate.fish`

On Windows using the Command Prompt: `venv\Scripts\activate.bat`

On Windows using PowerShell: `venv\Scripts\Activate.ps1`

```
python -m pip install -r requirements.txt
```

Uninstalling all packages:
```
python -m pip uninstall -r requirements.txt -y
```

Exporting pip packages to file from local environment:
```
python -m pip freeze --local > requirements.txt
```

Exporting pip packages to file:
```
python -m pip freeze > requirements.txt
```


Alternatively you can use pipenv to create virtual environment:
```
pip install pipenv
pipenv install
pipenv shell
```

### Running Docker container service

Basic usage:

```
docker-compose up -d --build
docker-compose run app
```

To run tests:
```
docker-compose run test pytest
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