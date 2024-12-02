#!/bin/bash
node=$1 
api_port=$2
printf "\nsed-service node: $node" 
printf "\nsed-service api-port: $api_port" 

sed s/%NODE%/$node/g base/service-template.yaml | \
sed s/%API_PORT%/$api_port/g > base/service.yaml 

sed s/%NODE%/$node/g overlays/service-template.yaml > overlays/service.yaml