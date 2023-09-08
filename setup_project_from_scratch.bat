@echo off
rmdir /s /q .\venv

docker system df
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker system prune -a
docker system df

python -m pip install --upgrade pip
python -m pip install virtualenv
python -m virtualenv venv

@REM .\venv\Scripts\activate.bat
venv\Scripts\Activate.ps1

python -m pip install -r requirements_dev.txt

docker-compose build
docker-compose run app