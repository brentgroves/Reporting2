#!/bin/bash
app=$1
ver=$2
api_port=$3

printf "\nbuild-reports-apps app: $app" 
printf "\nbuild-reports-apps ver: $ver" 
printf "\nbuild-reports-apps api_port: $api_port" 

rm dockerfile
cp dockerfiles/reports-apps/dockerfile-template ./dockerfile
# update the dockerfile
if [[ $app == "cron" ]]; then
    printf "\nbuilding reports-cron"
    sed -e "s/%WORK_DIR%/\/apps\/CronTab/g" \
    -e "/ENTRYPOINT \["cron", "-f"\]/s/^[ \t]*#[ \t]*//" \
    -e '/EXPOSE /s/^[ \t]*/#&/' \
    -e '/CMD \["flask", "run", "--host=0.0.0.0"\]/s/^[ \t]*/#&/' -i dockerfile    
    # build the docker image.
    # change the NODE build argument for ETL build
    # docker build --tag brentgroves/reports-etl:$ver --build-arg NODE=$node --build-arg CACHEBUST=$(date +%s) .
    docker build --tag brentgroves/reports-cron:$ver --build-arg CACHEBUST=$(date +%s) .
fi 
if [[ $app == "api" ]]; then
    printf "\nbuilding reports-api"
    sed -e '/%API_PORT%/$api_port/g' \    
    -e '/%WORK_DIR%/\/apps\/api/g' \    
    -e '/EXPOSE /s/^[ \t]*#[ \t]*//' \
    -e '/CMD \["flask", "run", "--host=0.0.0.0"\]/s/^[ \t]*#[ \t]*//' \
    -e '/ENTRYPOINT \["cron", "-f"\]/s/^[ \t]*/#&/' -i dockerfile
    docker build --tag brentgroves/reports-api:$ver --build-arg CACHEBUST=$(date +%s) .
fi

