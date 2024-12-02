#!/bin/bash
node=$1
mysql_port=$2
azure_dw=$3
ver=$4

printf "\nsed-deployment node: $node" 
printf "\nsed-deployment mysql_port: $mysql_port" 
printf "\nsed-deployment azure_dw: $azure_dw" 
printf "\nsed-deployment ver: $ver" 


sed s/%NODE%/$node/g base/deployment-template.yaml | \
sed s/%VER%/$ver/g > base/deployment.yaml 

sed s/%NODE%/$node/g overlays/deployment-template.yaml | \
sed s/%MYSQL_PORT%/$mysql_port/g | sed s/%AZURE_DW%/$azure_dw/g > overlays/deployment.yaml 

