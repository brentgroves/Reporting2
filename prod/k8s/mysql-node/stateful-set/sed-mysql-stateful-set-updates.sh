#!/bin/bash
app=$1
node=$2
node_port=$3
target_port=$4 
target_port_name=$5 
ver=$6

printf "\nsed-mysql-stateful-set-updates app: $app" 
printf "\nsed-mysql-stateful-set-updates node: $node" 
printf "\nsed-mysql-stateful-set-updates node_port: $node_port" 
printf "\nsed-mysql-stateful-set-updates target_port: $target_port" 
printf "\nsed-mysql-stateful-set-updates target_port_name: $target_port_name" 
printf "\nsed-mysql-stateful-set-updates ver: $ver" 

./sed-mysql-service.sh $app $node $node_port $target_port $target_port_name 
./sed-mysql-stateful-set.sh $app $node $target_port $target_port_name $ver