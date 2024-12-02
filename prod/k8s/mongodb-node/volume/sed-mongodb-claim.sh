#!/bin/bash
app=$1
node=$2

printf "\nsed-mongodb-claim app: $app" 
printf "\nsed-mongodb-claim node: $node" 

sed s/%APP%/$app/g base/claim-template.yaml | \
sed s/%NODE%/$node/g > base/claim.yaml

sed s/%APP%/$app/g overlay/claim-template.yaml | \
sed s/%NODE%/$node/g > overlay/claim.yaml

