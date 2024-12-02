#!/bin/bash
build_type=$1
file_name=$2

printf "\nsed-change-build-type build_type: $build_type" 
printf "\nsed-change-build-type file_name: $file_name" 

printf "\nupdating $file_name to $build_type build."

# Yes, to comment line containing specific string with sed, simply do:
# sed -i '/<pattern>/s/^/#/g' file
# And to uncomment it:
# sed -i '/<pattern>/s/^#//g' file
rm $file_name
cp ./template.py $file_name
if [[ $build_type == "prod" ]]; then
    sed -i /"#prod/s/#prod[ \t]*//g" $file_name
    # sed -i /"#prod/s/^[ \t]*#prod[ \t]*//g" $file_name
fi 
if [[ $build_type == "dev" ]]; then
    sed -i /"#dev/s/#dev[ \t]*//g" $file_name
    # sed -i /"#prod/s/^[ \t]*#prod[ \t]*//g" $file_name
fi 
# if [[ $app == "api" ]]; then
#     printf "\nbuilding reports-api"
#     sed -e '/%API_PORT%/$api_port/g' \    
#     -e '/%WORK_DIR%/\/apps\/api/g' \    
#     -e '/EXPOSE /s/^[ \t]*#[ \t]*//' \
#     -e '/CMD \["flask", "run", "--host=0.0.0.0"\]/s/^[ \t]*#[ \t]*//' \
#     -e '/ENTRYPOINT \["cron", "-f"\]/s/^[ \t]*/#&/' -i dockerfile
#     docker build --tag brentgroves/reports-api:$ver --build-arg CACHEBUST=$(date +%s) .
# fi

