#!/bin/bash
app=$1
node=$2
target_port=$3
target_port_name=$4
ver=$5

printf "\nsed-mongodb-deployment app: $app" 
printf "\nsed-mongodb-deployment node: $node" 
printf "\nsed-mongodb-deployment target_port: $target_port" 
printf "\nsed-mongodb-deployment target_port_name: $target_port_name" 
printf "\nsed-mongodb-deployment ver: $ver" 

sed s/%APP%/$app/g base/deployment-template.yaml | \
sed s/%NODE%/$node/g | \
sed s/%TARGET_PORT%/$target_port/g | \
sed s/%TARGET_PORT_NAME%/$target_port_name/g | \
sed s/%VER%/$ver/g > base/deployment.yaml

# sed s/%APP%/$app/g overlay/deployment-template.yaml | \
# sed s/%NODE%/$node/g | \
# sed s/%TARGET_PORT%/$target_port/g | \
# sed s/%TARGET_PORT_NAME%/$target_port_name/g | \
# sed s/%VER%/$ver/g > overlay/deployment.yaml

sed s/%APP%/$app/g overlay/deployment-template.yaml | \
sed s/%NODE%/$node/g | \
sed s/%VER%/$ver/g > overlay/deployment.yaml