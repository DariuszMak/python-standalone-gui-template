docker system df ; docker stop $(docker ps -a -q) ; docker rm $(docker ps -a -q) ; docker system prune -a ; docker system df

git fetch
git reset --hard
git clean -x -d -f

docker-compose run app