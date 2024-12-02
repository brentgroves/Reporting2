#!/bin/bash
app=$1
node=$2

printf "\nsed-mongodb-vol-updates app: $app" 
printf "\nsed-mongodb-vol-updates node: $node" 

./sed-mongodb-volume.sh $app $node  
./sed-mongodb-claim.sh $app $node