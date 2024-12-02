#!/bin/bash
app=$1
node=$2

printf "\nsed-mqtt-claim app: $app" 
printf "\nsed-mqtt-claim node: $node" 

sed s/%APP%/$app/g base/claim-template.yaml | \
sed s/%NODE%/$node/g> base/claim.yaml

sed s/%APP%/$app/g overlay/claim-template.yaml | \
sed s/%NODE%/$node/g> overlay/claim.yaml

# sed s/%VER%/$image_ver/g > base/deployment.yaml 

