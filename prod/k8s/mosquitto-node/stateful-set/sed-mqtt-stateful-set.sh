#!/bin/bash
app=$1
node=$2
target_port=$3
target_port_name=$4
ver=$5

printf "\nsed-mqtt-stateful-set app: $app" 
printf "\nsed-mqtt-stateful-set node: $node" 
printf "\nsed-mqtt-stateful-set target_port: $target_port" 
printf "\nsed-mqtt-stateful-set target_port_name: $target_port_name" 
printf "\nsed-mqtt-stateful-set ver: $ver" 

sed s/%APP%/$app/g base/stateful-set-template.yaml | \
sed s/%NODE%/$node/g | \
sed s/%TARGET_PORT%/$target_port/g | \
sed s/%TARGET_PORT_NAME%/$target_port_name/g | \
sed s/%VER%/$ver/g > base/stateful-set.yaml

sed s/%APP%/$app/g overlay/stateful-set-template.yaml | \
sed s/%NODE%/$node/g | \
sed s/%VER%/$ver/g > overlay/stateful-set.yaml
