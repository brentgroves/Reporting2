#!/bin/bash
node_name=$1
node_port=$2
service_name=$3 
app_name=$4

printf "\nsed-updates param 1: $1" 
printf "\nnode_name: $node_name" 
printf "\nsed-updates param 2: $2" 
printf "\nnode_port: $node_port" 
printf "\nsed-updates param 3: $3" 
printf "\nservice_name: $service_name" 
printf "\nsed-updates param 4: $4" 
printf "\napp_name: $app_name" 

./sed-service.sh $node_name $node_port $service_name $app_name 
./sed-deployment.sh $node_name $app_name