#!/bin/bash
app=$1
node=$2
mysql_port=$3
azure_dw=$4
ver=$5

printf "\nsed-mongodb-deployment app: $app" 
printf "\nsed-mongodb-deployment node: $node" 
printf "\nsed-mongodb-deployment mysql_port: $mysql_port" 
printf "\nsed-mongodb-deployment azure_dw: $azure_dw" 
printf "\nsed-mongodb-deployment ver: $ver" 

sed s/%APP%/$app/g base/deployment-template.yaml | \
sed s/%NODE%/$node/g | \
sed s/%VER%/$ver/g > base/deployment.yaml

sed s/%APP%/$app/g overlay/deployment-template.yaml | \
sed s/%NODE%/$node/g | \
sed s/%MYSQL_PORT%/$mysql_port/g | \
sed s/%AZURE_DW%/$azure_dw/g > overlay/deployment.yaml