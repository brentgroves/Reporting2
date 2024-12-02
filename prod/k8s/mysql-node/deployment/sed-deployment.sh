#!/bin/bash
node_name=$1
app_name=$2

printf "\nsed-deployment param 1: $1" 
printf "\nsed-deployment node_name: $node_name" 
printf "\nsed_deployment param 2: $2" 
printf "\nsed_deployment app_name: $app_name" 

sed s/%APP_NAME%/$app_name/g \
 base/deployment-template.yaml > base/deployment.yaml

sed s/%NODE_NAME%/$node_name/g \
 overlay/deployment-template.yaml | \
sed s/%APP_NAME%/$app_name/g > overlay/deployment.yaml

# sed s/%VER%/$image_ver/g > base/deployment.yaml 

