#!/bin/bash
# ./sed-volume.sh dev reports11 30011 1 reports11 30311 reports
build=$1
mysql_host=$2
mysql_port=$3
azure_dw=$4
mongo_host=$5
mongo_port=$6
mongo_db=$7

printf "\nsed_volume build: $build" 
printf "\nsed_volume mysql_host: $mysql_host" 
printf "\nsed_volume mysql_port: $mysql_port" 
printf "\nsed_volume azure_dw: $azure_dw" 
printf "\nsed_volume mongo_host: $mongo_host" 
printf "\nsed_volume mongo_port: $mongo_port" 
printf "\nsed_volume mongo_db: $mongo_db" 

cd ~/src/Reporting/prod/volume/misc
./sed-script-start-py.sh $build $mysql_host $mysql_port $azure_dw script-start.py
cd ~/src/Reporting/prod/volume/misc
./sed-script-end-py.sh $build $mysql_host $mysql_port $azure_dw script-end.py

cd ~/src/Reporting/prod/volume/AccountingYearCategoryType
./sed-change-build-py.sh $build $mysql_host $mysql_port $azure_dw AccountingYearCategoryType.py

cd ~/src/Reporting/prod/volume/AccountingAccount
./sed-change-build-py.sh $build $mysql_host $mysql_port $azure_dw AccountAccount.py

cd ~/src/Reporting/prod/volume/AccountingPeriod
./sed-change-build-py.sh $build $mysql_host $mysql_port $azure_dw AccountingPeriod.py

cd ~/src/Reporting/prod/volume/AccountingPeriodRanges
./sed-change-build-py.sh $build $mysql_host $mysql_port $azure_dw AccountingPeriodRanges.py

cd ~/src/Reporting/prod/volume/AccountingStartPeriodUpdate
./sed-change-build-py.sh $build $mysql_host $mysql_port $azure_dw AccountingStartPeriodUpdate.py

cd ~/src/Reporting/prod/volume/AccountingBalanceAppendPeriodRange
./sed-change-build-py.sh $build $mysql_host $mysql_port $azure_dw AccountingBalanceAppendPeriodRange.py

cd ~/src/Reporting/prod/volume/AccountActivitySummaryGetOpenPeriodRange
./sed-change-build-py.sh $build $mysql_host $mysql_port $azure_dw AccountActivitySummaryGetOpenPeriodRange.py

cd ~/src/Reporting/prod/volume/AccountPeriodBalanceRecreatePeriodRange
./sed-change-build-py.sh $build $mysql_host $mysql_port $azure_dw AccountPeriodBalanceRecreatePeriodRange.py

cd ~/src/Reporting/prod/volume/AccountPeriodBalanceRecreateOpenPeriodRange
./sed-change-build-py.sh $build $mysql_host $mysql_port $azure_dw AccountPeriodBalanceRecreateOpenPeriodRange.py


# cd ~/src/Reporting/prod/volume/AccountPeriodBalanceToMongoDB
# ./sed-change-build-py.sh $build $mysql_host $mysql_port $mongo_host $mongo_port $mongo_db AccountPeriodBalanceToMongoDB.py


# cd ~/src/Reporting/prod/volume/CronTab
# ./sed-CronTabUpdate.sh $build $mysql_host $mysql_port 
# ./sed-crontab-base.sh $build $mysql_host $mysql_port $azure_dw
# cd ../modules
# ./sed-insert-crontab.sh $build $mysql_host $mysql_port
# ./sed-insert-queue.sh $build $mysql_host $mysql_port
# ./sed-update-crontab.sh $build $mysql_host $mysql_port

