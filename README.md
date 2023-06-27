# Python Standalone GUI template

## Dependencies

- Python 3.10.10
- Docker

### Local configuration:
```commandline
python -m pip install --upgrade pip
python -m pip install virtualenv
python -m virtualenv venv
```

On Unix or MacOS, using the bash shell: `source venv/bin/activate`

On Unix or MacOS, using the csh shell: `source venv/bin/activate.csh`

On Unix or MacOS, using the fish shell: `source venv/bin/activate.fish`

On Windows using the Command Prompt: `venv\Scripts\activate.bat`

On Windows using PowerShell: `venv\Scripts\Activate.ps1`

###### Or just set it in IDE as current environment

```commandline
python -m pip install -r requirements.txt
```

Uninstalling all packages:
```commandline
pip freeze > packages.txt; pip uninstall -y -r packages.txt; del packages.txt
```

Exporting pip packages to file from local environment:
```commandline
python -m pip freeze --local > requirements.txt
```

Exporting pip packages to file:
```commandline
python -m pip freeze > requirements.txt
```


Alternatively you can use pipenv to create virtual environment:
```commandline
pip install pipenv
pipenv install
pipenv shell
```

## Running Docker container service

Basic usage:

```commandline
docker-compose up -d --build
docker-compose run app
```

To run tests:
```commandline
docker-compose run test
```

## Another useful Docker commands

Regular usage:

```commandline
docker compose up
```

or in detached mode:

```commandline
docker compose up -d
```

Build images before starting containers and force recreate containers even if their configuration and image haven't changed:
```commandline
docker compose up --build --force-recreate --always-recreate-deps
```

After the job is done (optionally)
```commandline
docker compose down
```

## Docker issues

### "Vmmem" process consuming a lot of memory
To free some resources temporarily:

```commandline
wsl --shutdown
```

In order to set up max memory range create a file `%UserProfile%/.wslconfig` and write:

```commandline
[wsl2]
memory=8GB
```

It is recommended also to turn off paging file of virtual memory in operating system.

## GUI files specification

<mark>.qrc</mark> - resources file edited in QT Designer

<mark>.ui</mark> - QT Designer form

<mark>ui_*.py</mark> - QT Designer generated tools