#!/bin/bash
app=$1
ver=$2
mongo_port=$3

printf "\nbuild-mongodb app: $app" 
printf "\nbuild-mongodb ver: $ver" 
printf "\nbuild-mongodb port: $mongo_port" 

rm dockerfile
cp dockerfiles/mongodb/dockerfile-template ./dockerfile
# update the dockerfile
if [[ $app == "mongodb" ]]; then
    printf "\nbuilding mongodb"
    sed -e "s#%MONGO_PORT%#$mongo_port#g" \
    -e "s#%WORK_DIR%#/apps#g" -i dockerfile
    docker build --tag brentgroves/mongodb:$ver --build-arg CACHEBUST=$(date +%s) .
fi

