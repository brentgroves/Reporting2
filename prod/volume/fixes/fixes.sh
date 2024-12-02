#!/bin/bash
mysql_host=$1
mysql_port=$2
azure_dw=$3

printf "\ncrontab-init mysql_host: $mysql_host" 
printf "\ncrontab-init mysql_port: $mysql_port" 
printf "\ncrontab-init azure_dw: $azure_dw\n" 

./crontab-init.sh $mysql_host $mysql_port $azure_dw

# https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/#known-issues
# This can't be done in the dockerfile
cp ./resolv.conf /etc/resolv.conf 


