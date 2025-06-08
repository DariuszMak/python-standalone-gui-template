# Python Standalone GUI template


## Dependencies

- Python 3.10.10
- Docker


## Setup entire project from scratch (Windows PowerShell)

Make sure, that everything is committed or stashed and (optionally):

```commandline
git reset --hard HEAD ; 
git clean -x -d -f ; 
```

##### Setup local environment and install dependencies

```commandline
Remove-Item -Recurse -Force .\venv ; 

python -m pip install --upgrade pip ; 
python -m pip install virtualenv ; 
python -m virtualenv venv ; 

# .\venv\Scripts\activate.bat ; 
venv\Scripts\Activate.ps1 ; 

python -m pip install -r requirements_dev.txt ; 
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

##### Docker should compile ```ui``` files, but you can do it manually

```commandline
$env:PYTHONPATH="." ; 
venv\Scripts\Activate.ps1 ; 

python src\gui_setup.py ; 
```


### Running executable application via PyInstaller (install dependencies)

In order to generate executable application, run:
```commandline
$env:PYTHONPATH="." ; 
venv\Scripts\Activate.ps1 ; 

pyinstaller --clean .\standalone_build\standalone_build.spec ; 
```


## Run tests:

```commandline
pytest -vv ; 
```

Run tests with coverage report:

```commandline
pytest . --cov=. ; 
```


## Code autoformat

##### Mypy

```commandline
mypy . ; 
mypy --strict . ; 
```

##### Isort

```commandline
isort . ; 
```

##### Black

```commandline
black . ; 
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
docker-compose run app . /opt/venv/bin/activate ; pip install -r requirements_dev.txt ; pytest . --cov=. ; 
```


## GUI files specification

<mark>.qrc</mark> - resources file edited in QT Designer

<mark>.ui</mark> - QT Designer form

<mark>ui_*.py</mark> - QT Designer generated tools
