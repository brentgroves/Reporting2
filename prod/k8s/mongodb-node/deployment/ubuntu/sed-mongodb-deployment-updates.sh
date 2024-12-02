#!/bin/bash
app=$1
node=$2
node_port=$3
target_port=$4
target_port_name=$5
mysql_port=$6
azure_dw=$7
ver=$8

printf "\nsed-mongodb-deployment-updates app: $app" 
printf "\nsed-mongodb-deployment-updates node: $node" 
printf "\nsed-mongodb-deployment-updates node_port: $node_port" 
printf "\nsed-mongodb-deployment-updates target_port: $target_port" 
printf "\nsed-mongodb-deployment-updates target_port_name: $target_port_name" 

printf "\nsed-mongodb-deployment-updates mysql_port: $mysql_port" 
printf "\nsed-mongodb-deployment-updates azure_dw: $azure_dw" 

printf "\nsed-mongodb-deployment-updates ver: $ver" 

./sed-mongodb-service.sh $app $node $node_port $target_port $target_port_name 
./sed-mongodb-deployment.sh $app $node $mysql_port $azure_dw $ver