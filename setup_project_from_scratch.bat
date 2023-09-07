@echo off
@REM git fetch
@REM git reset --hard
@REM git clean -x -d -f

rmdir /s /q .\venv

python -m pip install --upgrade pip
python -m pip install virtualenv
python -m virtualenv venv

@REM .\venv\Scripts\activate.bat
venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt

docker system df
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker system prune -a
docker system df

docker-compose run app