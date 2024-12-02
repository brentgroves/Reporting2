#!/bin/bash
build=$1
mysql_host=$2
mysql_port=$3


printf "\nsed-CronTabUpdate.sh build: $build" 
printf "\nsed-CronTabUpdate.sh mysql_host: $mysql_host" 
printf "\nsed-CronTabUpdate.sh mysql_port: $mysql_port" 

# sed -e '/BBB/s/^/#/g' -i file
if [[ $build == 'dev' ]]
then
  printf '\ndev build'
  sed -e '/%DEV%/s/%DEV%//' CronTabUpdate-template.sh | \
  sed -e "/%MYSQL_HOST%/s/%MYSQL_HOST%/$mysql_host/" | \
  sed -e "/%MYSQL_PORT%/s/%MYSQL_PORT%/$mysql_port/" | \
  sed -e '/%PROD%/s/^/#/' > CronTabUpdate.sh 
else
  printf '\nprod build'
  sed -e '/%DEV%/s/^/#/' CronTabUpdate-template.sh | \
  sed -e "/%MYSQL_HOST%/s/%MYSQL_HOST%/$mysql_host/" | \
  sed -e "/%MYSQL_PORT%/s/%MYSQL_PORT%/$mysql_port/" | \
  sed -e '/%PROD%/s/%PROD%//' > CronTabUpdate.sh 
fi

# if [[ $build == 'dev' ]]
# then
#   printf '\ndev build'
#   sed -e '/%DEV%/s/%DEV%//' CronTabUpdate-template.py | \
#   sed -e "/%MYSQL_HOST%/s/%MYSQL_HOST%/$mysql_host/" | \
#   sed -e "/%MYSQL_PORT%/s/%MYSQL_PORT%/$mysql_port/" | \
#   sed -e '/%PROD%/s/^/#/' > CronTabUpdate.py 
# else
#   printf '\nprod build'
#   sed -e '/%DEV%/s/^/#/' CronTabUpdate-template.py | \
#   sed -e "/%MYSQL_HOST%/s/%MYSQL_HOST%/$mysql_host/" | \
#   sed -e "/%MYSQL_PORT%/s/%MYSQL_PORT%/$mysql_port/" | \
#   sed -e '/%PROD%/s/%PROD%//' > CronTabUpdate.py 
# fi

# sed s/%NODE%/$node/g overlays/deployment-template.yaml | \
# sed s/%MYSQL_PORT%/$mysql_port/g | sed s/%AZURE_DW%/$azure_dw/g > overlays/deployment.yaml 

