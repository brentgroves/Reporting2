#!/bin/bash
node_name=$1
node_port=$2
service_name=$3 
app_name=$4

printf "\nsed-service param 1: $1" 
printf "\nnode_name: $node_name" 
printf "\nsed-service param 2: $2" 
printf "\nnode_port: $node_port" 
printf "\nsed-service param 3: $3" 
printf "\nservice_name: $service_name" 
printf "\nsed-service param 4: $4" 
printf "\napp_name: $app_name" 

sed s/%SERVICE_NAME%/$service_name/g \
 base/service-template.yaml | \
sed s/%APP_NAME%/$app_name/g > base/service.yaml 

sed s/%SERVICE_NAME%/$service_name/g \
 overlay/service-template.yaml | \
sed s/%NODE_PORT%/$node_port/g > overlay/service.yaml 