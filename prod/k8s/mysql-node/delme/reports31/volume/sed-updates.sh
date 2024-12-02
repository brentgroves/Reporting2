#!/bin/bash
volume_name=$1 
claim_name=$2
printf "\n\$1: $1" 
printf "\n\$volume_name: $volume_name" 
printf "\n\$2: $2" 
printf "\n\$claim_name: $claim_name" 

./sed-volume.sh $volume_name  
./sed-claim.sh $claim_name