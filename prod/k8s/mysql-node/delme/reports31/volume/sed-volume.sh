#!/bin/bash
volume_name=$1 
printf "\n\$1: $1" 
printf "\n\$volume_name: $volume_name" 
sed s/%VOLUME_NAME%/$volume_name/g \
 volume-template.yaml > base/volume.yaml 