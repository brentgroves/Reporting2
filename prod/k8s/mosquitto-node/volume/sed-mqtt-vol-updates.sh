#!/bin/bash
app=$1
node=$2

printf "\nsed-mqtt-vol-updates app: $app" 
printf "\nsed-mqtt-vol-updates node: $node" 

./sed-mqtt-vol.sh $app $node   
./sed-mqtt-claim.sh $app $node