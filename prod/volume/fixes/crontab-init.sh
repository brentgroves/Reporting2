#!/bin/bash
mysql_host=$1
mysql_port=$2
azure_dw=$3
printf "\ncrontab-init mysql_host: $mysql_host" 
printf "\ncrontab-init mysql_port: $mysql_port" 
printf "\ncrontab-init azure_dw: $azure_dw\n" 

sed s/%MYSQL_HOST%/$mysql_host/g /apps/CronTab/crontab-base-template | \
sed s/%MYSQL_PORT%/$mysql_port/g | \
sed s/%AZURE_DW%/$azure_dw/g > /apps/CronTab/crontab-base  

# run app to 
crontab /apps/CronTab/crontab-base


