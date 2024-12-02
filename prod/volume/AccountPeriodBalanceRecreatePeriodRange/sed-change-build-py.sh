#!/bin/bash
#!/bin/bash
build=$1
mysql_host=$2
mysql_port=$3
azure_dw=$4
file=$5

printf "\nsed-AccountPeriodBalanceRecreatePeriodRange build: $build" 
printf "\nsed-AccountPeriodBalanceRecreatePeriodRange mysql_host: $mysql_host" 
printf "\nsed-AccountPeriodBalanceRecreatePeriodRange mysql_port: $mysql_port" 
printf "\nsed-AccountPeriodBalanceRecreatePeriodRange azure_dw: $azure_dw" 
printf "\nsed-AccountPeriodBalanceRecreatePeriodRange file: $file" 

if [[ $build == 'dev' ]]
then
  printf '\ndev build'
  sed -e '/%DEV%/s/%DEV%/  /' template.py | \
  sed -e "/%MYSQL_HOST%/s/%MYSQL_HOST%/$mysql_host/" | \
  sed -e "/%MYSQL_PORT%/s/%MYSQL_PORT%/$mysql_port/" | \
  sed -e "/%AZURE_DW%/s/%AZURE_DW%/$azure_dw/" | \
  sed -e '/%PROD%/s/^/#/' > $file
else
  printf '\nprod build'
  sed -e '/%DEV%/s/^/#/' template.py | \
  sed -e "/%MYSQL_HOST%/s/%MYSQL_HOST%/$mysql_host/" | \
  sed -e "/%MYSQL_PORT%/s/%MYSQL_PORT%/$mysql_port/" | \
  sed -e "/%AZURE_DW%/s/%AZURE_DW%/$azure_dw/" | \
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



