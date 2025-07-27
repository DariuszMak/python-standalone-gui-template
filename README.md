# Python Standalone GUI template

[![Preview Image](images/Runtime_screenshot.png)](https://github.com/DariuszMak/python-standalone-gui-template/releases/download/0.5.0/GUI_client.exe)

## Requirements

- [UV](https://github.com/astral-sh/uv) package manager
- [Docker Desktop](https://www.docker.com/products/docker-desktop)


## Setup project from scratch (PowerShell):

```commandline
deactivate ; 
clear ; 

git reset --hard HEAD ; 
git clean -x -d -f ; 

uv python install 3.11 ; 
uv python pin 3.11 ; 
uv sync --dev --no-cache ; 
uv lock ; 

docker system df ; 
docker stop $(docker ps -a -q) ; 
docker rm -f $(docker ps -a -q) ; 
docker system prune --volumes -a -f ; 
docker system df ; 

docker-compose run --build app ; 

$env:PYTHONPATH="." ; 
.venv\Scripts\Activate.ps1 ; 

uv run ruff format test\ src\ --exclude 'moc_.*\.py|files_rc\.py' ; 
uv run ruff check --fix test\ src\ --exclude 'moc_.*\.py|files_rc\.py' ; 
uv run ruff check --fix --unsafe-fixes test\ src\ --exclude 'moc_.*\.py|files_rc\.py' ; 
uv run ruff check --fix --select I test\ src\ --exclude 'moc_.*\.py|files_rc\.py' ; 

uv run pip-audit ; 
uv run ruff check test\ src\ --exclude 'moc_.*\.py|files_rc\.py' ; 
uv run ruff format --check test\ src\ --exclude 'moc_.*\.py|files_rc\.py' ; 
uv run mypy --explicit-package-bases test\ src\ --exclude 'moc_.*\.py|files_rc\.py' ; 

pytest test/ --cov=. ; 
docker-compose run app sh -c "uv sync --dev --locked --no-cache && uv run pytest test/ --cov=." ; 

uv sync --no-dev --locked --no-cache ; 

docker-compose run --rm app sh -c "uv sync --dev --locked --no-cache && uv run pyinstaller --clean ./standalone_build/standalone_build_linux.spec && cp -r dist/* linux_distribution/"

uv run pyinstaller --clean .\standalone_build\standalone_build.spec ; 

Start-Process ".\dist\GUI_client.exe" ; 
Start-Sleep -Seconds 10 ; 
Start-Process "http://127.0.0.1:8000/schema/redoc" ; 
Start-Process "http://127.0.0.1:8000/schema/swagger" ; 
newman run Python_GUI.postman_collection.json --environment Windows.postman_environment.json --bail

Start-Process wsl -ArgumentList 'bash', '-c', 'export DISPLAY=$(grep nameserver /etc/resolv.conf | awk "{print $2}"):0 && ./linux_distribution/GUI_client'
Start-Sleep -Seconds 10 ; 
Start-Process "http://127.0.0.1:8001/schema/redoc" ; 
Start-Process "http://127.0.0.1:8001/schema/swagger" ; 
newman run Python_GUI.postman_collection.json --environment Linux.postman_environment.json --bail

uv sync --dev --locked --no-cache ; 
```


## Setup entire project from scratch (Windows PowerShell)

Make sure, that everything is committed or stashed and (optionally):

```commandline
git reset --hard HEAD ; 
git clean -x -d -f ; 
```

#### Install Python 3.11:

```commandline
uv python install 3.11 ; 
uv python pin 3.11 ; 
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
uv sync --dev --no-cache ; 
uv lock ; 
```

##### Docker should compile ```ui``` files, but as an alternative you can do it manually

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
uv run pytest -vv test/ ; 
```

Run tests with coverage report:

```commandline
pytest test/ --cov=. ; 
```

Run tests in Docker:
```commandline
docker-compose run app sh -c "uv sync --dev --locked --no-cache  && uv run pytest test/ --cov=." ; 
```

Run Newman tests from saved collection (run application before execution):
```commandline
newman run collections\Python_GUI.postman_collection.json ; 
```


## Edit `ui` forms with QT Designer:

```commandline
uv run pyqt6-tools designer src\ui\forms\main_window.ui ;
uv run pyqt6-tools designer src\ui\forms\warning_dialog.ui ;
```


## Code linting

```commandline
$env:PYTHONPATH="." ; 
.venv\Scripts\Activate.ps1 ; 

clear ; 

uv run pip-audit ;  
uv run ruff check test\ src\ --exclude 'moc_.*\.py|files_rc\.py' ; 
uv run ruff format --check test\ src\ --exclude 'moc_.*\.py|files_rc\.py' ; 
uv run mypy --explicit-package-bases test\ src\ --exclude 'moc_.*\.py|files_rc\.py' ; 
# uv run mypy --explicit-package-bases --check-untyped-defs . ; 
```


## Code autoformat

```commandline
$env:PYTHONPATH="." ; 
.venv\Scripts\Activate.ps1 ; 

clear ; 

uv run ruff format test\ src\ --exclude 'moc_.*\.py|files_rc\.py' ; 

uv run ruff check --fix test\ src\ --exclude 'moc_.*\.py|files_rc\.py' ; 
uv run ruff check --fix --unsafe-fixes test\ src\ --exclude 'moc_.*\.py|files_rc\.py' ; 
uv run ruff check --fix --select I test\ src\ --exclude 'moc_.*\.py|files_rc\.py' ; 
```

## Running Docker container service

##### Build and run
```commandline
docker-compose run --build app ; 
```

## GUI files specification

<mark>.qrc</mark> - resources file edited in QT Designer

<mark>.ui</mark> - QT Designer form

<mark>ui_*.py</mark> - QT Designer generated tools
