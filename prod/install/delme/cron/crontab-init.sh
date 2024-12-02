#!/bin/bash
mysql_host=$1
mysql_port=$2
azure_dw=$3
printf "\nsed-cron mysql_host: $mysql_host" 
printf "\nsed-cron mysql_port: $mysql_port" 
printf "\nsed-cron azure_dw: $azure_dw\n" 

sed s/%MYSQL_HOST%/$mysql_host/g /app/crontab/etl-template | \
sed s/%MYSQL_PORT%/$mysql_port/g | \
sed s/%AZURE_DW%/$azure_dw/g > /app/crontab/etl-crontab  

# run app to 
crontab /app/crontab/etl-crontab


