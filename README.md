# Python Standalone GUI template

## Shortest sequece of commands to setup project from scratch:

```commandline
uv python pin 3.11 ; 

git reset --hard HEAD ; 
git clean -x -d -f ; 

docker system df ; 
docker stop $(docker ps -a -q) ; 
docker rm $(docker ps -a -q) ; 
docker system prune -a ; 
docker system df ; 
docker-compose run --build app ; 

uv sync --dev ; 

$env:PYTHONPATH="." ; 
.venv\Scripts\Activate.ps1 ; 

pytest . --cov=. ; 

uv run pyinstaller --clean .\standalone_build\standalone_build.spec ; 
```

## Requirements

- [UV](https://github.com/astral-sh/uv) package manager
- [Docker Desktop](https://www.docker.com/products/docker-desktop)

#### Install Python 3.11:

```commandline
uv python install 3.11 ; 
uv python pin 3.11 ; 
```


## Setup entire project from scratch (Windows PowerShell)

Make sure, that everything is committed or stashed and (optionally):

```commandline
git reset --hard HEAD ; 
git clean -x -d -f ; 
```

##### Run the application (compile mocks) from Docker

```commandline
docker system df ; 
docker stop $(docker ps -a -q) ; 
docker rm $(docker ps -a -q) ; 
docker system prune -a ; 
docker system df ; 

docker-compose run --build app ; 
```

##### Setup local environment and install dependencies

```commandline 
uv python pin 3.11 ; 
uv sync --dev ; 
```

##### Docker should compile ```ui``` files, but you can do it manually

```commandline
$env:PYTHONPATH="." ; 
.venv\Scripts\Activate.ps1 ; 

uv run python src\gui_setup.py ; 
```

### Running application natively

```commandline
$env:PYTHONPATH="." ; 
.venv\Scripts\Activate.ps1 ; 

uv run python src\main.py ; 
```

### Running executable application via PyInstaller (generate UI forms before !!!)

In order to generate executable application, run:
```commandline
$env:PYTHONPATH="." ; 
.venv\Scripts\Activate.ps1 ; 

uv run pyinstaller --clean .\standalone_build\standalone_build.spec ; 
```


## Run tests:

```commandline
uv run pytest -vv ; 
```

Run tests with coverage report:

```commandline
pytest . --cov=. ; 
```


## Edit `ui` forms with QT Designer:

```commandline
uv run pyqt6-tools designer src\ui\forms\main_window.ui ;
uv run pyqt6-tools designer src\ui\forms\warning_dialog.ui ;
```


## Code autoformat

```commandline
$env:PYTHONPATH="." ; 
.venv\Scripts\Activate.ps1 ; 

uv run pip-audit ; 

uv run ruff check ; 
uv run mypy --explicit-package-bases . ; 
uv run mypy --explicit-package-bases --check-untyped-defs ; 

uv run ruff check --fix ; 
uv run ruff check --fix --unsafe-fixes ; 
uv run ruff check --fix --select I ; 
uv run ruff format ; 
```

## Running Docker container service

##### Build project
```commandline
docker-compose build ; 
```

##### Run app
```commandline
docker-compose run app ; 
```

##### Build before running
```commandline
docker-compose run --build app ; 
```

##### Run tests in Docker
```commandline
docker-compose run app sh -c "uv sync --dev && uv run pytest . --cov=." ; 
```


## GUI files specification

<mark>.qrc</mark> - resources file edited in QT Designer

<mark>.ui</mark> - QT Designer form

<mark>ui_*.py</mark> - QT Designer generated tools
