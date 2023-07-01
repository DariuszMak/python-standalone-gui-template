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

- On Unix or MacOS, using the bash shell: `source venv/bin/activate`
- On Unix or MacOS, using the csh shell: `source venv/bin/activate.csh`
- On Unix or MacOS, using the fish shell: `source venv/bin/activate.fish`
- On Windows using the Command Prompt: `venv\Scripts\activate.bat`
- On Windows using PowerShell: `venv\Scripts\Activate.ps1`

Or just set it in IDE as current environment.

```commandline
python -m pip install -r requirements.txt
```

## Installing pre-commit hooks

File ```.pre-commit-config.yaml``` contains the definition of checks that will be run during the pipeline deployment
phase. In order to keep the pipeline happy ;) (and also to make sure we conform to one, centrally defined coding
standard) every developer should install the pre-commit-hooks in their local environment to ensure that every commit
that is pushed to the remote repository passes the checks.

- first, install pre-commit library into your python environment:

```commandline
pip install pre-commit
```

- then, install ```pre-commit``` hooks defined in the ```.yaml``` file:

```commandline
pre-commit install
```

This should automatically detect and install all dependencies required by ```.pre-commit-config.yaml```, and also now
pre-commit will run automatically on every ```git commit```!

- run pre-commit for all files:

```commandline
pre-commit run --all-files
```
- update hooks:

```commandline
pre-commit install-hooks
```

- if you want to ignore errors from changes, use "n" flag:

```commandline
git commit -n -m "commit message"
```
## Another useful pip commands

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

## PyCharm not finding unit tests fix
```commandline
python -m pip install nose
```
Open `Run/Debug Configurations` > `Python tests` > click + button > Pytest > In target: choose script path > e.g.: `D:/Repos/python-standalone-gui-template/test`

Run tests again with new configuration.

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

After the job is done (optionally):
```commandline
docker compose down
```

To prune docker:
```commandline
docker system prune --all
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

## GUI files specification

<mark>.qrc</mark> - resources file edited in QT Designer

<mark>.ui</mark> - QT Designer form

<mark>ui_*.py</mark> - QT Designer generated tools
