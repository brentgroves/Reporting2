#!/bin/bash
app=$1
node=$2

printf "\nsed-mysql-vol-updates app: $app" 
printf "\nsed-mysql-vol-updates node: $node" 

./sed-mysql-volume.sh $app $node  
./sed-mysql-claim.sh $app $node