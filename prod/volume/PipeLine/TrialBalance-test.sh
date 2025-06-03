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



# export username='mg.odbcalbion'
# export password='Mob3xalbion'
# export username2='mgadmin'
# export password2='WeDontSharePasswords1!'
# export username3='root'
# export password3='password'
# export username4='MGEdonReportsws@plex.com'
# export password4='9f45e3d-67ed-'
# export MYSQL_HOST='reports11'
# export MYSQL_PORT='30331'
# export AZURE_DW='0'

pipeline="TrialBalance"
script="none"
export em=""
export emline=""
export dm=""
export line=""
export tm=""
export result=0
export reportId=11

# https://stackoverflow.com/questions/14481521/get-the-id-of-inserted-document-in-mongo-database-in-nodejs
# https://stackoverflow.com/questions/14481521/get-the-id-of-inserted-document-in-mongo-database-in-nodejs
# https://stackoverflow.com/questions/14481521/get-the-id-of-inserted-document-in-mongo-database-in-nodejs
# https://databasefaqs.com/how-to-get-id-from-mongodb-after-insert/
# https://databasefaqs.com/how-to-get-id-from-mongodb-after-insert/
# https://databasefaqs.com/how-to-get-id-from-mongodb-after-insert/
# ./TrialBalance-test.sh "TB" "bgroves@buschegroup.com" "202201" "202301" "once"

# import pymongo

# myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017")
# mydb = myclient['mydatabase']
# mycol = mydb["customers"]

# mydict = { "name": "Jack", "address": "Lowstreet 27, USA" }

# x = mycol.insert_one(mydict)

# print(x.inserted_id)
# The source command reads and executes commands from the file 
# specified as its argument in the current shell environment. 
# It is useful to load functions, 
# variables, and configuration files into shell scripts.
# echo "pwd: $(pwd)"export start_period=$3

# script="GetReportId"
# printf "\nStarting: $script\n" 1>&4
# cd ../GetReportId
# source GetReportId.sh 
# cd ../PipeLine
# printf "\n$script result=$result"
# printf "\nreportId=$reportId"
# https://gist.github.com/mihow/9c7f559807069a03e302605691f85572
# set -a
# export $(echo $(cat .env | sed 's/#.*//g'| xargs) | envsubst)

# source <(cat .env | sed -e '/^#/d;/^\s*$/d' -e "s/'/'\\\''/g" -e "s/=\(.*\)/='\1'/g")
# printf "\nreportId=$reportId"
# set +a

# set: set [-abefhkmnptuvxBCHP] [-o option-name] [--] [arg ...]

# reset variables
em=""
emline=""
dm=""
line=""
tm=""

if [[ $result -eq 0 ]]
then # if/then branch
  script="AccountingYearCategoryType"
  printf "\nStarting: $script\n" 
  printf "\nStarting: $script\n" 1>&4
  cd ../AccountingYearCategoryType
  source AccountingYearCategoryType.sh 
  printf "\n$script result=$result"
fi

# reset variables
em=""
emline=""
dm=""
line=""
tm=""

# if [[ $result -eq 0 ]]
# then # if/then branch
#   exec 6<>tm-msg
#   read input <&6 && echo "$script time: ${input}" 1>&4
#   exec 6<>tm-msg
#   script="AccountingAccount"
#   printf "\nStarting: $script\n" 1>&4
#   cd ../AccountingAccount
#   source AccountingAccount.sh 
#   printf "\n$script result=$result"
# fi


# reset variables
em=""
emline=""
dm=""
line=""
tm=""

# if [[ $result -eq 0 ]]
# then # if/then branch
#   exec 6<>tm-msg
#   read input <&6 && echo "$script time: ${input}" 1>&4
#   exec 6<>tm-msg
#   script="AccountingPeriod"
#   printf "\nStarting: $script\n" 1>&4
#   cd ../AccountingPeriod
#   source AccountingPeriod.sh 
#   printf "\n$script result=$result"
# fi


# reset variables
em=""
emline=""
dm=""
line=""
tm=""

# if [[ $result -eq 0 ]]
# then # if/then branch
#   exec 6<>tm-msg
#   read input <&6 && echo "$script time: ${input}" 1>&4
#   exec 6<>tm-msg
#   script="AccountingPeriodRanges"
#   printf "\nStarting: $script\n" 1>&4
#   cd ../AccountingPeriodRanges
#   source AccountingPeriodRanges.sh 
#   printf "\n$script result=$result"
# fi

# reset variables
em=""
emline=""
dm=""
line=""
tm=""

# DONT USE: THIS FUNCTION STILL CALLS MYSQL!!!!!!!!!!!!!!!!!!
# if [ $result -eq 0 ] && [ $start_period_update -eq 1 ]
# then # if/then branch
#   exec 6<>tm-msg
#   read input <&6 && echo "$script time: ${input}" 1>&4
#   exec 6<>tm-msg
#   script="AccountingStartPeriodUpdate"
#   printf "\nStarting: $script\n" 1>&4
#   cd ../AccountingStartPeriodUpdate
#   source AccountingStartPeriodUpdate.sh 
#   printf "\n$script result=$result"
# fi

# reset variables
em=""
emline=""
dm=""
line=""
tm=""

# set pcn
pcn=123681

# if [[ $result -eq 0 ]]
# then # if/then branch
#   exec 6<>tm-msg
#   read input <&6 && echo "$script time: ${input}" 1>&4
#   exec 6<>tm-msg
#   script="AccountingBalanceAppendPeriodRange"
#   printf "\nStarting: $script\n" 1>&4
#   cd ../AccountingBalanceAppendPeriodRange
#   source AccountingBalanceAppendPeriodRange.sh 
#   printf "\n$script result=$result"
# fi

# # reset variables
# em=""
# emline=""
# dm=""
# line=""
# tm=""

# # set pcn
# pcn=300758
# if [[ $result -eq 0 ]]
# then # if/then branch
#   script="AccountingBalanceAppendPeriodRange"
#   cd ../AccountingBalanceAppendPeriodRange
#   source AccountingBalanceAppendPeriodRange.sh 
# fi

# reset variables
em=""
emline=""
dm=""
line=""
tm=""

# # set pcn
pcn=123681
# https://askubuntu.com/questions/1403837/how-do-i-use-openssl-1-1-1-in-ubuntu-22-04
# if [[ $result -eq 0 ]]
# then # if/then branch
#   exec 6<>tm-msg
#   read input <&6 && echo "$script time: ${input}" 1>&4
#   exec 6<>tm-msg
#   script="AccountActivitySummaryGetOpenPeriodRange"
#   printf "\nStarting: $script\n" 1>&4
#   cd ../AccountActivitySummaryGetOpenPeriodRange
#   source AccountActivitySummaryGetOpenPeriodRange.sh 
#   printf "\n$script result=$result"
# fi

# # # reset variables
# # em=""
# # emline=""
# # dm=""
# # line=""
# # tm=""

# # # set pcnen
# # pcn=300758

# # if [[ $result -eq 0 ]]
# # then # if/then branch
# #   script="AccountActivitySummaryGetOpenPeriodRange"
# #   cd ../AccountActivitySummaryGetOpenPeriodRange
# #   source AccountActivitySummaryGetOpenPeriodRange.sh 
# # fi


# reset variables
em=""
emline=""
dm=""
line=""
tm=""

# set pcn
pcn=123681

# if [[ $result -eq 0 ]]
# then # if/then branch
#   exec 6<>tm-msg
#   read input <&6 && echo "$script time: ${input}" 1>&4
#   exec 6<>tm-msg
#   script="AccountPeriodBalanceRecreatePeriodRange"
#   printf "\nStarting: $script\n" 1>&4
#   cd ../AccountPeriodBalanceRecreatePeriodRange
#   source AccountPeriodBalanceRecreatePeriodRange.sh 
#   printf "\n$script result=$result"
# fi

# # reset variables
# em=""
# emline=""
# dm=""
# line=""
# tm=""

# # set pcn
# # pcn=300758

# if [[ $result -eq 0 ]]
# then # if/then branch
#   exec 6<>tm-msg
#   read input <&6 && echo "$script time: ${input}" 1>&4
#   exec 6<>tm-msg
#   script="AccountPeriodBalanceRecreatePeriodRange"
#   printf "\nStarting: $script\n" 1>&4
#   cd ../AccountPeriodBalanceRecreatePeriodRange
#   source AccountPeriodBalanceRecreatePeriodRange.sh 
#   echo "$script result=$result"
# fi

# reset variables
em=""
emline=""
dm=""
line=""
tm=""

# # set pcn
pcn=123681
# # WATCH: THERE WAS AN ERROR IN THIS SCRIPT FOR MYSQL THERE WAS A 202213 PERIOD  
# # "AccountPeriodBalanceRecreateOpenPeriodRange"

# if [[ $result -eq 0 ]]
# then # if/then branch
#   exec 6<>tm-msg
#   read input <&6 && echo "$script time: ${input}" 1>&4
#   exec 6<>tm-msg
#   script="AccountPeriodBalanceRecreateOpenPeriodRange"
#   printf "\nStarting: $script\n" 1>&4
#   cd ../AccountPeriodBalanceRecreateOpenPeriodRange
#   source AccountPeriodBalanceRecreateOpenPeriodRange.sh 
#   printf "\n$script result=$result"
# fi

# # # reset variables
# # em=""
# # emline=""
# # dm=""
# # line=""
# # tm=""

# # # set pcn
# # pcn=300758

# # if [[ $result -eq 0 ]]
# # then # if/then branch
# #   script="AccountPeriodBalanceRecreateOpenPeriodRange"
# #   cd ../AccountPeriodBalanceRecreateOpenPeriodRange
# #   source AccountPeriodBalanceRecreateOpenPeriodRange.sh 
# # fi

# # reset variables
# em=""
# emline=""
# dm=""
# line=""
# tm=""

# if [[ $result -eq 0 ]]
# then # if/then branch
#   exec 6<>tm-msg
#   read input <&6 && echo "$script time: ${input}" 1>&4
#   exec 6<>tm-msg
#   script="TrialBalanceExcel"
#   printf "\nStarting: $script\n" 1>&4
#   cd ../TrialBalanceExcel
#   source TrialBalanceExcel.sh 
#   echo "$script result=$result"
#   echo "TrialBalanceExcel.sh result=$result"
# fi 

# # # Open file descriptor
# # exec 4>dbg-msg 

# # if [[ $result -ne 0 ]]
# # then # if/then branch
# #   printf "\nPipeline terminated at $script" 1>&4
# #   printf "Pipeline terminated on $script script." | mail -s "MCP Pipeline Failure" bgroves@buschegroup.com
# # else
# #   printf "\nPipeline Successful all scripts completed." 1>&4
# #   printf "Pipeline successful all scripts have completed." | mail -s "MCP Pipeline Success" bgroves@buschegroup.com
# # fi

# # if [[ $result -ne 0 ]]
# # then # if/then branch
# #   printf "$script script failed. \nerror message: $em \ndebug messages: $dm \ntime=$tm" | mail -s "MCP Script Failure" bgroves@buschegroup.com
# # fi
# if [[ $result -eq 0 ]]
# then # if/then branch
#   exec 6<>tm-msg
#   read input <&6 && echo "$script time: ${input}" 1>&4
#   exec 6<>tm-msg
#   script="AccountPeriodBalanceRecreateOpenPeriodRange"
#   printf "\nStarting: $script\n" 1>&4
#   cd ../AccountPeriodBalanceRecreateOpenPeriodRange
#   source AccountPeriodBalanceRecreateOpenPeriodRange.sh 
#   echo "$script result=$result"
# fi

# cd ../PipeLine 

# # echo "pwd: $(pwd)"
# exec 3<>error-msg
# while IFS= read -r emline
# do
#   em="${em}"$'\n'"${emline}"  
#   #  p="${var1}"$'\n'"${var2}"
#   # echo "$line"
# done <&3
# # echo "$script error message=$em"

# exec 4<>dbg-msg
# while IFS= read -r line
# do
#   dm="${dm}"$'\n'"${line}"  
#   #  p="${var1}"$'\n'"${var2}"
#   # echo "$line"
# done <&4
# # echo "$script debug messages=$dm"

# exec 6<>tm-msg
# read tm <&6 && echo "$script time: ${tm}" 1>&4
# # echo "$script time=$tm"

# if [[ $result -ne 0 ]]
# then # if/then branch
#   printf "\n$pipeline pipeline terminated on $script script.\n$script script failed. \nerror message: $em \ndebug messages: $dm \nlast script time=$tm" 1>&4
#   printf "$pipeline pipeline terminated on $script script.\n$script script failed. \nerror message: $em \ndebug messages: $dm \nlast script time=$tm" | mail -s "$pipeline Pipeline Failure" bgroves@buschegroup.com
# else
#   printf "\n$pipeline pipeline successful all scripts completed." 1>&4
#   printf "$pipeline pipeline successful all scripts have completed." | mail -s "$pipeline Pipeline Success" bgroves@buschegroup.com
# fi

# # printf "$pipeline pipeline terminated on $script script.\n$script script failed. \nerror message: $em \ndebug messages: $dm \nlast script time=$tm" | mail -s "$pipeline Pipeline Failure" bgroves@buschegroup.com

# # printf "$pipeline pipeline terminated on $script script.\n$script script failed. \nerror message: $em \ndebug messages: $dm \nlast script time=$tm" 

# # # Close FD
# # As far as I can see, exec 3>&- and exec 3<&- are the same and 
# # can be used on any file descriptor, regardless of how it was opened. 
# exec 3>&- 4>&- 5>&- 6>&- 

