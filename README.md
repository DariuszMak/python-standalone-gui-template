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

- On Unix or macOS, using the bash shell: `source venv/bin/activate`
- On Unix or macOS, using the csh shell: `source venv/bin/activate.csh`
- On Unix or macOS, using the fish shell: `source venv/bin/activate.fish`
- On Windows using the Command Prompt: `venv\Scripts\activate.bat`
- On Windows using PowerShell: `venv\Scripts\Activate.ps1`

Or just set it in IDE as current environment and then:

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

- unistall pre-commit:
```commandline
pre-commit uninstall
```

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

## Running Docker container service

Build project:
```commandline
docker-compose build
```

Run app:
```commandline
docker-compose run app
```

Build before running:
```commandline
docker-compose run --build app
```

## Setup entire project from scratch (Windows)

Make sure, that everything is committed or stashed and (optionally):

```commandline
git clean -x -d -f
```

then

```commandline
.\setup_project_from_scratch.bat
```


In order to replace generated ```ui``` files manually (if docker didn't do it before) run:
```commandline
venv\Scripts\Activate.ps1 ; .\app\ui\auto_generated\replace_generated.bat
```

## GUI files specification

<mark>.qrc</mark> - resources file edited in QT Designer

<mark>.ui</mark> - QT Designer form

<mark>ui_*.py</mark> - QT Designer generated tools
