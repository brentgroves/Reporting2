#!/bin/bash
claim_name=$1

printf "\n\$1: $1" 
printf "\n\$claim_name: $claim_name" 

sed s/%CLAIM_NAME%/$claim_name/g \
 claim-template.yaml > base/claim.yaml
# sed s/%VER%/$image_ver/g > base/deployment.yaml 

