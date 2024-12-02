#!/bin/bash
# ./sed-mysql-service.sh mysql 0 30010 3306 mysql-port

app=$1
ordinal=$2
node_port=$3
target_port=$4
target_port_name=$5

printf "\nsed-mysql-service app: $app" 
printf "\nsed-mysql-service ordinal: $ordinal" 
printf "\nsed-mysql-service node_port: $node_port" 
printf "\nsed-mysql-service target_port: $target_port" 
printf "\nsed-mysql-service target_port_name: $target_port_name" 


sed s/%APP%/$app/g base/service-template.yaml | \
sed s/%ORDINAL%/$ordinal/g | \
sed s/%NODE_PORT%/$node_port/g | \
sed s/%TARGET_PORT%/$target_port/g | \
sed s/%TARGET_PORT_NAME%/$target_port_name/g > base/service.yaml 

