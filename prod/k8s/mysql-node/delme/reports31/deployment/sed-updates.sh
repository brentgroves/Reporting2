#!/bin/bash
service_name=$1 
app_name=$2
# printf "\n\$1: $1" 1>&4
# printf "\n\$2: $2" 1>&4

./sed-service.sh $service_name $app_name 
./sed-deployment.sh $app_name