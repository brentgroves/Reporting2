#!/bin/bash
app=$1
node=$2
node_port=$3
target_port=$4
target_port_name=$5
ver=$6

printf "\nsed-mongodb-deployment-updates app: $app" 
printf "\nsed-mongodb-deployment-updates node: $node" 
printf "\nsed-mongodb-deployment-updates node_port: $node_port" 
printf "\nsed-mongodb-deployment-updates target_port: $target_port" 
printf "\nsed-mongodb-deployment-updates target_port_name: $target_port_name" 
printf "\nsed-mongodb-deployment-updates ver: $ver" 

./sed-mongodb-service.sh $app $node $node_port $target_port $target_port_name 
./sed-mongodb-deployment.sh $app $node $target_port $target_port_name $ver