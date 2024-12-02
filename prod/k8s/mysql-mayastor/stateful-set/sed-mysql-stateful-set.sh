#!/bin/bash
# ./sed-mysql-stateful-set.sh mysql 3306 mysql-port 5Gi 8.0
app=$1
target_port=$2
target_port_name=$3
size=$4
ver=$5

printf "\nsed-mysql-stateful-set app: $app" 
printf "\nsed-mysql-stateful-set target_port: $target_port" 
printf "\nsed-mysql-stateful-set target_port_name: $target_port_name" 
printf "\nsed-mysql-stateful-set size: $size" 
printf "\nsed-mysql-stateful-set ver: $ver" 

sed s/%APP%/$app/g base/stateful-set-template.yaml | \
sed s/%TARGET_PORT%/$target_port/g | \
sed s/%TARGET_PORT_NAME%/$target_port_name/g | \
sed s/%SIZE%/$size/g | \
sed s/%VER%/$ver/g > base/stateful-set.yaml

sed s/%APP%/$app/g overlay/stateful-set-template.yaml | \
sed s/%SIZE%/$size/g > overlay/stateful-set.yaml
