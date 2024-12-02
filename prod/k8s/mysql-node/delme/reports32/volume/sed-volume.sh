#!/bin/bash
node_name=$1 
printf "\n\sed-volume param 1: $1" 
printf "\n\sed-volume node_name: $node_name" 

volume_name=$2 
printf "\n\sed-volume param 2: $2" 
printf "\n\sed-volumen volume_name: $volume_name" 

sed s/%VOLUME_NAME%/$volume_name/g \
 base/volume-template.yaml > base/volume.yaml 

sed s/%NODE_NAME%/$node_name/g \
  overlay/volume-template.yaml | \
sed s/%VOLUME_NAME%/$volume_name/g > overlay/volume.yaml 