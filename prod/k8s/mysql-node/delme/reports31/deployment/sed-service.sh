#!/bin/bash
service_name=$1 
app_name=$2
printf "\n\$1: $1" 
printf "\n\$2: $2" 
printf "\n\$service_name: $service_name" 
printf "\n\$app_name: $app_name" 
sed s/%SERVICE_NAME%/$service_name/g \
 service-template.yaml | \
sed s/%APP_NAME%/$app_name/g > base/service.yaml 