#!/bin/bash
# mysql_host=$1
# mysql_port=$2
# azure_dw=$3
ver=$1

# printf "\nbuild-crontab-volume mysql_host: $mysql_host" 
# printf "\nbuild-crontab-volume mysql_port: $mysql_port" 
# printf "\nbuild-crontab-volume azure_dw: $azure_dw" 
printf "\nbuild-crontab-init ver: $ver\n" 

# mysql_host=$1
# mysql_port=$2
# azure_dw=$3
# run the following from a k8s cmd before copying crontab to
# the shared volume  
# cd init/cron  
# ./sed-cron.sh 
# ./sed-cron.sh $mysql_host $mysql_port $azure_dw 
# cd ../..
rm dockerfile
cp dockerfiles/crontab-init/dockerfile .

docker build --tag brentgroves/reports-crontab-init:$ver --build-arg CACHEBUST=$(date +%s) .

