#!/bin/bash
build=$1
mysql_host=$2
mysql_port=$3

printf "\nsed_insert_crontab build: $build" 
printf "\nsed_insert_crontab mysql_host: $mysql_host" 
printf "\nsed_insert_crontab mysql_port: $mysql_port" 
# sed -e '/BBB/s/^/#/g' -i file
if [[ $build == 'dev' ]]
then
  printf '\ndev build'
  sed -e "/%DEV%/s/%DEV%//" insert_crontab_template.py | \
  sed -e "/%PROD%/s/^/#/" | \
  sed -e "/%MYSQL_HOST%/s/%MYSQL_HOST%/$mysql_host/" | \
  sed -e "/%MYSQL_PORT%/s/%MYSQL_PORT%/$mysql_port/" > insert_crontab.py 
else
  printf '\nprod build'
  sed -e "/%DEV%/s/^/#/" insert_crontab_template.py | \
  sed -e "/%PROD%/s/%PROD%//" | \
  sed -e "/%MYSQL_HOST%/s/%MYSQL_HOST%/$mysql_host/" | \
  sed -e "/%MYSQL_PORT%/s/%MYSQL_PORT%/$mysql_port/" > insert_crontab.py 
fi

# sed s/%NODE%/$node/g overlays/deployment-template.yaml | \
# sed s/%MYSQL_PORT%/$mysql_port/g | sed s/%AZURE_DW%/$azure_dw/g > overlays/deployment.yaml 

