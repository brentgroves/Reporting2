#!/bin/bash
# pushd ~/src/Reporting/prod/volume/PipeLine
# 04-2022 to 04-2023
# TB-202204_to_202304_on_05-09_DM
# usage ./TrialBalance-test.sh "TB" "bgroves@buschegroup.com" "202204" "202304" 0 "once"
# If start_period_update = 1 the AccountingStartPeriodUpdate script will run
./truncate-logs.sh

# https://copyconstruct.medium.com/bash-redirection-fun-with-descriptors-e799ec5a3c16
# Open file descriptor
exec 3<>error-msg 4<>dbg-msg 5>error-num 6<>tm-msg 

printf "\n\$1: $1" 1>&4
printf "\n\$2: $2" 1>&4
printf "\n\$3: $3" 1>&4
printf "\n\$4: $4" 1>&4
printf "\n\$5: $5" 1>&4
printf "\n\$6: $6" 1>&4

export report_name=$1
export email=$2
export start_period=$3
export end_period=$4
export start_period_update=$5
export frequency=$5

printf "\nreport_name: $report_name" 
printf "\nemail: $email" 
printf "\nstart_period: $start_period" 
printf "\nend_period: $end_period" 
printf "\nstart_period_update: $start_period_update" 
printf "\nfrequency: $frequency\n" 


# Get pcn from http request in the future
export pcn="123681"
export pcn_list="123681"
# export pcn_list="123681,300758"
export username=$(</etc/lastpass/username)
export password=$(</etc/lastpass/password)
export username2=$(</etc/lastpass/username2)
export password2=$(</etc/lastpass/password2)
export username3=$(</etc/lastpass/username3)
export password3=$(</etc/lastpass/password3)
export username4=$(</etc/lastpass/username4)
export password4=$(</etc/lastpass/password4)
export MYSQL_HOST=$(</etc/lastpass/MYSQL_HOST)
export MYSQL_PORT=$(</etc/lastpass/MYSQL_PORT)
export AZURE_DW=$(</etc/lastpass/AZURE_DW)
export MYSQL_HOST=$(</etc/lastpass/MYSQL_HOST)
export MYSQL_PORT=$(</etc/lastpass/MYSQL_PORT)
export AZURE_DW=$(</etc/lastpass/AZURE_DW)
export MONGO_HOST=$(</etc/lastpass/MONGO_HOST)
export MONGO_PORT=$(</etc/lastpass/MONGO_PORT)
export MONGO_DB=$(</etc/lastpass/MONGO_DB)

printf "\npcn: $pcn" 
printf "\npcn_list: $pcn_list" 
printf "\nusername: $username" 
printf "\npassword: $password" 
printf "\nusername2: $username2" 
printf "\npassword2: $password2" 
printf "\nusername3: $username3" 
printf "\npassword3: $password3"
printf "\nusername4: $username4" 
printf "\npassword4: $password4"
printf "\nMYSQL_HOST: $MYSQL_HOST" 
printf "\nMYSQL_PORT: $MYSQL_PORT" 
printf "\nAZURE_DW: $AZURE_DW" 
printf "\nMONGO_HOST: $MONGO_HOST" 
printf "\nMONGO_PORT: $MONGO_PORT" 
printf "\nMONGO_DB: $MONGO_DB" 

