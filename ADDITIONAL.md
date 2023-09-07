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
