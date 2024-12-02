#!/bin/bash
#!/bin/bash
build=$1
mysql_host=$2
mysql_port=$3
mongo_host=$4
mongo_port=$5
mongo_db=$6
file=$7

printf "\nsed-change-build build: $build" 
printf "\nsed-change-build mysql_host: $mysql_host" 
printf "\nsed-change-build mysql_port: $mysql_port" 
printf "\nsed-change-build mongo_host: $mongo_host" 
printf "\nsed-change-build mongo_port: $mongo_port" 
printf "\nsed-change-build mongo_db: $mongo_db" 
printf "\nsed-change-build file: $file" 


if [[ $build == 'dev' ]]
then
  printf '\ndev build'
  sed -e '/%DEV%/s/%DEV%/  /' template.py | \
  sed -e "/%MYSQL_HOST%/s/%MYSQL_HOST%/$mysql_host/" | \
  sed -e "/%MYSQL_PORT%/s/%MYSQL_PORT%/$mysql_port/" | \
  sed -e "/%MONGO_HOST%/s/%MONGO_HOST%/$mongo_host/" | \
  sed -e "/%MONGO_PORT%/s/%MONGO_PORT%/$mongo_port/" | \
  sed -e "/%MONGO_DB%/s/%MONGO_DB%/$mongo_db/" | \
  sed -e '/%PROD%/s/^/#/' > $file
fi
if [[ $build_type == "prod" ]]
then
  printf '\nprod build'
  sed -e '/%DEV%/s/^/#/' template.py | \
  sed -e "/%MYSQL_HOST%/s/%MYSQL_HOST%/$mysql_host/" | \
  sed -e "/%MYSQL_PORT%/s/%MYSQL_PORT%/$mysql_port/" | \
  sed -e "/%MONGO_HOST%/s/%MONGO_HOST%/$mongo_host/" | \
  sed -e "/%MONGO_PORT%/s/%MONGO_PORT%/$mongo_port/" | \
  sed -e "/%MONGO_DB%/s/%MONGO_DB%/$mongo_db/" | \
  sed -e '/%PROD%/s/%PROD%/  /' > $file
fi

# Yes, to comment line containing specific string with sed, simply do:
# sed -i '/<pattern>/s/^/#/g' file
# And to uncomment it:
# sed -i '/<pattern>/s/^#//g' file
# rm $file_name
# cp ./template.py $file_name
# if [[ $build_type == "prod" ]]; then
#     sed -i /"#prod/s/#prod[ \t]*//g" $file_name
#     # sed -i /"#prod/s/^[ \t]*#prod[ \t]*//g" $file_name
# fi 
# if [[ $build_type == "dev" ]]; then
#     sed -i /"#dev/s/#dev[ \t]*//g" $file_name
#     # sed -i /"#prod/s/^[ \t]*#prod[ \t]*//g" $file_name
# fi 



