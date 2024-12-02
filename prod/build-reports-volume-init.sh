#!/bin/bash
ver=$1
printf "\nbuild-reports-volume-init ver: $ver" 

rm dockerfile
cp dockerfiles/reports-volume-init/dockerfile .

docker build --tag brentgroves/reports-volume-init:$ver --build-arg CACHEBUST=$(date +%s) .

