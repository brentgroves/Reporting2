#!/bin/bash
# ./sed-lastpass-yaml.sh reports11 30010 reports11 30311 reports 1 
# ./sed-lastpass-yaml.sh reports31 30031 reports32 30331 reports 1 
mysql_host=$1
mysql_port=$2
mongo_host=$3
mongo_port=$4
mongo_db=$5
azure_dw=$6

printf "\nsed-lastpass-yaml mysql_host: $mysql_host" 
printf "\nsed-lastpass-yaml mysql_port: $mysql_port" 
printf "\nsed-lastpass-yaml mongo_host: $mongo_host" 
printf "\nsed-lastpass-yaml mongo_port: $mongo_port" 
printf "\nsed-lastpass-yaml mongo_db: $mongo_db" 
printf "\nsed-lastpass-yaml azure_dw: $azure_dw" 

sed -e "/%MYSQL_HOST%/s/%MYSQL_HOST%/$mysql_host/" template.yaml | \
sed -e "/%MYSQL_PORT%/s/%MYSQL_PORT%/$mysql_port/" | \
sed -e "/%MONGO_HOST%/s/%MONGO_HOST%/$mongo_host/" | \
sed -e "/%MONGO_PORT%/s/%MONGO_PORT%/$mongo_port/" | \
sed -e "/%MONGO_DB%/s/%MONGO_DB%/$mongo_db/" | \
sed -e "/%AZURE_DW%/s/%AZURE_DW%/$azure_dw/" > lastpass.yaml

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



