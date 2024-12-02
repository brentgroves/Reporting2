#!/bin/bash
app_name=$1

printf "\n\$1: $1" 
printf "\n\$app_name: $2" 

sed s/%APP_NAME%/$app_name/g \
 deployment-template.yaml > base/deployment.yaml
# sed s/%VER%/$image_ver/g > base/deployment.yaml 

