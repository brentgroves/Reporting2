#!/bin/bash
build=$1
mysql_host=$2
mysql_port=$3
azure_dw=$4

printf "\nsed_crontab-base build: $build" 
printf "\nsed_crontab-base mysql_host: $mysql_host" 
printf "\nsed_crontab-base mysql_port: $mysql_port" 
printf "\nsed_crontab-base azure_dw: $azure_dw" 
# sed -e '/BBB/s/^/#/g' -i file
if [[ $build == 'dev' ]]
then
  printf '\ndev build'
  # sed -e "/%DEV%/s/%DEV%//" crontab-base-template | \
  # sed -e "/%PROD%/s/^/#/" | \
  sed -e "/%MYSQL_HOST%/s/%MYSQL_HOST%/$mysql_host/" | \
  sed -e "/%MYSQL_PORT%/s/%MYSQL_PORT%/$mysql_port/" | \
  sed -e "/%AZURE_DW%/s/%AZURE_DW%/$azure_dw/" > crontab-base > crontab-base-dev
else
  printf '\nprod build'
  # sed -e "/%DEV%/s/^/#/" crontab-base-template | \
  # sed -e "/%PROD%/s/%PROD%//" | \
  sed -e "/%MYSQL_HOST%/s/%MYSQL_HOST%/$mysql_host/" | \
  sed -e "/%MYSQL_PORT%/s/%MYSQL_PORT%/$mysql_port/" | \
  sed -e "/%AZURE_DW%/s/%AZURE_DW%/$azure_dw/" > crontab-base > crontab-base
fi

# sed s/%NODE%/$node/g overlays/deployment-template.yaml | \
# sed s/%MYSQL_PORT%/$mysql_port/g | sed s/%AZURE_DW%/$azure_dw/g > overlays/deployment.yaml 

