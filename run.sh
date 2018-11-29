
docker volume create --name=db_volume || { echo 'failed to create volume'; exit 1; }
docker-compose build || { echo 'failed to build'; exit 1; }
docker-compose up || { echo 'failed to run'; exit 1; }
