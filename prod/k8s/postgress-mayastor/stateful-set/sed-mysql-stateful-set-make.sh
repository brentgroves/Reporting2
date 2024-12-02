#!/bin/bash
# ./sed-mysql-stateful-set-make.sh mysql 0 30010 3306 mysql-port 5Gi 8.0

app=$1
ordinal=$2
node_port=$3
target_port=$4 
target_port_name=$5 
size=$6
ver=$7

printf "\nsed-mysql-stateful-set-make app: $app" 
printf "\nsed-mysql-stateful-set-make ordinal: $ordinal" 
printf "\nsed-mysql-stateful-set-make node_port: $node_port" 
printf "\nsed-mysql-stateful-set-make target_port: $target_port" 
printf "\nsed-mysql-stateful-set-make target_port_name: $target_port_name" 
printf "\nsed-mysql-stateful-set-make ver: $size" 
printf "\nsed-mysql-stateful-set-make ver: $ver" 

./sed-mysql-service.sh $app $ordinal $node_port $target_port $target_port_name 
cp ./base/service.yaml ./output/service.yaml
./sed-mysql-stateful-set.sh $app $target_port $target_port_name $size $ver
