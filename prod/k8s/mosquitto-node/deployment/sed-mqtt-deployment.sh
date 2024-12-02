#!/bin/bash
app=$1
node=$2
target_port=$3
target_port_name=$4

printf "\nsed-mqtt-deployment app: $app" 
printf "\nsed-mqtt-deployment node: $node" 
printf "\nsed-mqtt-deployment target_port: $target_port" 
printf "\nsed-mqtt-deployment target_port_name: $target_port_name" 

sed s/%APP%/$app/g base/deployment-template.yaml | \
sed s/%NODE%/$node/g | \
sed s/%TARGET_PORT%/$target_port/g | \
sed s/%TARGET_PORT_NAME%/$target_port_name/g > base/deployment.yaml

sed s/%APP%/$app/g overlay/deployment-template.yaml | \
sed s/%NODE%/$node/g | \
sed s/%TARGET_PORT_NAME%/$target_port_name/g > overlay/deployment.yaml

