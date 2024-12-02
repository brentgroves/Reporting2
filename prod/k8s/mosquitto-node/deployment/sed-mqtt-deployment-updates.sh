#!/bin/bash
app=$1
node=$2
node_port=$3
target_port=$4
target_port_name=$5

printf "\nsed-mqtt-deployment-updates app: $app" 
printf "\nsed-mqtt-deployment-updates node: $node" 
printf "\nsed-mqtt-deployment-updates node_port: $node_port" 
printf "\nsed-mqtt-deployment-updates target_port: $target_port" 
printf "\nsed-mqtt-deployment-updates target_port_name: $target_port_name" 

./sed-mqtt-service.sh $app $node $node_port $target_port $target_port_name 
./sed-mqtt-deployment.sh $app $node $target_port $target_port_name