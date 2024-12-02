#!/bin/bash
node=$1
api_port=$2
mysql_port=$3
azure_dw=$4
ver=$5

printf "\nsed-k8s-updates node: $node" 
printf "\nsed-k8s-updates api_port: $api_port" 
printf "\nsed-k8s-updates mysql_port: $mysql_port" 
printf "\nsed-k8s-updates azure_dw: $azure_dw" 
printf "\nsed-k8s-updates ver: $ver" 


./sed-service.sh $node $api_port 
./sed-deployment.sh $node $mysql_port $azure_dw $ver