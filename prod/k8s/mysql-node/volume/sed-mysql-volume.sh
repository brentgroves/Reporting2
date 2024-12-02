#!/bin/bash
app=$1
node=$2 
printf "\nsed-mysql-volume app: $app" 
printf "\nsed-mysql-volume node: $node" 

sed s/%APP%/$app/g base/volume-template.yaml | \
sed s/%NODE%/$node/g > base/volume.yaml

sed s/%APP%/$app/g overlay/volume-template.yaml | \
sed s/%NODE%/$node/g > overlay/volume.yaml 
