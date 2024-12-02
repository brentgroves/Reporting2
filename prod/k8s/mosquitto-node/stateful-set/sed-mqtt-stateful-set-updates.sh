#!/bin/bash
app=$1
node=$2
node_port=$3
target_port=$4
target_port_name=$5
ver=$6

printf "\nsed-mqtt-stateful-set-updates app: $app" 
printf "\nsed-mqtt-stateful-set-updates node: $node" 
printf "\nsed-mqtt-stateful-set-updates node_port: $node_port" 
printf "\nsed-mqtt-stateful-set-updates target_port: $target_port" 
printf "\nsed-mqtt-stateful-set-updates target_port_name: $target_port_name" 
printf "\nsed-mqtt-stateful-set-updates ver: $ver" 

./sed-mqtt-service.sh $app $node $node_port $target_port $target_port_name 
./sed-mqtt-stateful-set.sh $app $node $target_port $target_port_name $ver