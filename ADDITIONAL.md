# Additional issues


## Useful pip commands

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
Open `Run/Debug Configurations` > `Python tests` > click + button > Pytest > In target: choose script path > e.g.: `D:/Repos/python-standalone-gui-template`

Run tests again with new configuration.

## Add to system path if needed

If you don't want to use local environment for files e.g. ```pyside6-rcc.exe``` or ```pyside6-uic.exe```, you can add these paths to system path:
```commandline
C:\Users\%Username%\AppData\Roaming\Python\Python310\Scripts
C:\Users\%Username%\AppData\Roaming\Python\Python310\site-packages

C:\Program Files\Python310\Scripts
C:\Program Files\Python310\Lib\site-packages
C:\Program Files\Python310\
```

## Prune project

First approach:

```commandline
git fetch
git reset --hard
git clean -x -d -f
```

Second approach:

```commandline
git fetch --prune origin
git reset --hard origin/master
git clean -f -d
```

## Useful Docker commands

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

Prune docker:
```commandline
docker system df ; docker stop $(docker ps -a -q) ; docker rm $(docker ps -a -q) ; docker system prune -a ; docker system df
```

## Docker issues

### "Vmmem" process consuming a lot of memory
Free some resources temporarily:

```commandline
wsl --shutdown
```

In order to set up max memory range create a file `%UserProfile%/.wslconfig` and write:

```commandline
[wsl2]
memory=8GB
```
