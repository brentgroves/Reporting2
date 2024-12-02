#!/bin/bash
node_name=$1
volume_name=$2 
claim_name=$3

printf "\nsed-updates param 1: $1" 
printf "\nsed-updates node_name: $node_name" 
printf "\nsed-updates param 2: $2" 
printf "\nvolume_name: $volume_name" 
printf "\nsed-updates param 3: $3" 
printf "\nclaim_name: $claim_name" 

./sed-volume.sh $node_name $volume_name  
./sed-claim.sh $claim_name