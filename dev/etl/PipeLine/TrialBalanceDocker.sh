#!/bin/bash
# python debug1.py
# ./debug2.sh

./truncate-logs.sh

# https://copyconstruct.medium.com/bash-redirection-fun-with-descriptors-e799ec5a3c16
# Open file descriptor
exec 3<>error-msg 4<>dbg-msg 5>error-num 6<>tm-msg 

printf "\n\$1: $1" 1>&4
printf "\n\$2: $2" 1>&4
printf "\n\$3: $3" 1>&4
printf "\n\$4: $4" 1>&4
printf "\n\$5: $5" 1>&4

export report_name=$1
export etl_only=$2
export email=$3
export start_period=$4
export end_period=$5

# for k8s debugging
# printf "\nTrialBalance:report_name: $report_name" 1>&4
# printf "\nTrialBalance:etl_only=$etl_only" 1>&4
# printf "\nTrialBalance:email: $email" 1>&4
# printf "\nTrialBalance:start_period: $start_period" 1>&4
# printf "\nTrialBalance:end_period: $end_period" 1>&4
# printf "\nTrialBalance:frequency: $frequency \n" 1>&4

# for localhost debuggin
printf "\nTrialBalance:report_name: $report_name" 
printf "\nTrialBalance:etl_only=$etl_only" 
printf "\nTrialBalance:email: $email" 
printf "\nTrialBalance:start_period: $start_period" 
printf "\nTrialBalance:end_period: $end_period" 


pipeline="TrialBalance"
export em=""
export emline=""
export dm=""
export line=""
export tm=""
export result=0

# Get pcn from http request in the future
# export pcn="123681"
# export pcn_list="123681"
# export pcn_list="123681,300758"
# export username=$(</etc/db-user-pass/username)
# export password=$(</etc/db-user-pass/password)
# export username2=$(</etc/db-user-pass/username2)
# export password2=$(</etc/db-user-pass/password2)
# export username3=$(</etc/db-user-pass/username3)
# export password3=$(</etc/db-user-pass/password3)
# export username4=$(</etc/db-user-pass/username4)
# export password4=$(</etc/db-user-pass/password4)
# following will already be set from k8s env:
# export MYSQL_HOST='reports31'
# export MYSQL_PORT='30031'
# export AZURE_DW='0'

export pcn="123681"
export pcn_list="123681,300758"
export username='mg.odbcalbion'
export password='Mob3xalbion'
export username2='mgadmin'
export password2='WeDontSharePasswords1!'
export username3='root'
export password3='password'
export username4='MGEdonReportsws@plex.com'
export password4='9f45e3d-67ed-'
export MYSQL_HOST='reports31'
export MYSQL_PORT='30031'
export AZURE_DW='0'

script="none"


export em=""
export emline=""
export dm=""
export line=""
export tm=""
export result=0 

# The source command reads and executes commands from the file 
# specified as its argument in the current shell environment. 
# It is useful to load functions, 
# variables, and configuration files into shell scripts.
# echo "pwd: $(pwd)"
script="AccountingYearCategoryType"
printf "\nStarting: $script\n" 1>&4
cd ../AccountingYearCategoryType
source AccountingYearCategoryType.sh 
echo "$script result=$result"

#DEBUG STATEMENT TO END PIPELINE
result=0 

# reset variables
em=""
emline=""
dm=""
line=""
tm=""


if [[ $result -eq 0 ]]
then # if/then branch
  exec 6<>tm-msg
  read input <&6 && echo "$script time: ${input}" 1>&4
  exec 6<>tm-msg
  script="AccountingAccount"
  printf "\nStarting: $script\n" 1>&4
  cd ../AccountingAccount
  source AccountingAccount.sh 
  echo "$script result=$result"
fi

# reset variables
em=""
emline=""
dm=""
line=""
tm=""

if [[ $result -eq 0 ]]
then # if/then branch
  exec 6<>tm-msg
  read input <&6 && echo "$script time: ${input}" 1>&4
  exec 6<>tm-msg
  script="AccountingPeriod"
  printf "\nStarting: $script\n" 1>&4
  cd ../AccountingPeriod
  source AccountingPeriod.sh 
  echo "$script result=$result"
fi


# reset variables
em=""
emline=""
dm=""
line=""
tm=""

if [[ $result -eq 0 ]]
then # if/then branch
  exec 6<>tm-msg
  read input <&6 && echo "$script time: ${input}" 1>&4
  exec 6<>tm-msg
  script="AccountingPeriodRanges"
  printf "\nStarting: $script\n" 1>&4
  cd ../AccountingPeriodRanges
  source AccountingPeriodRanges.sh 
  echo "$script result=$result"
fi

# reset variables
em=""
emline=""
dm=""
line=""
tm=""

if [[ $result -eq 0 ]]
then # if/then branch
  exec 6<>tm-msg
  read input <&6 && echo "$script time: ${input}" 1>&4
  exec 6<>tm-msg
  script="AccountingStartPeriodUpdate"
  printf "\nStarting: $script\n" 1>&4
  cd ../AccountingStartPeriodUpdate
  source AccountingStartPeriodUpdate.sh 
  echo "$script result=$result"
fi

# reset variables
em=""
emline=""
dm=""
line=""
tm=""

# set pcn
pcn=123681

if [[ $result -eq 0 ]]
then # if/then branch
  exec 6<>tm-msg
  read input <&6 && echo "$script time: ${input}" 1>&4
  exec 6<>tm-msg
  script="AccountingBalanceAppendPeriodRange"
  printf "\nStarting: $script\n" 1>&4
  cd ../AccountingBalanceAppendPeriodRange
  source AccountingBalanceAppendPeriodRange.sh 
  echo "$script result=$result"

fi

# reset variables
em=""
emline=""
dm=""
line=""
tm=""

# set pcn
pcn=123681

if [[ $result -eq 0 ]]
then # if/then branch
  exec 6<>tm-msg
  read input <&6 && echo "$script time: ${input}" 1>&4
  exec 6<>tm-msg
  script="AccountActivitySummaryGetOpenPeriodRange"
  printf "\nStarting: $script\n" 1>&4
  cd ../AccountActivitySummaryGetOpenPeriodRange
  source AccountActivitySummaryGetOpenPeriodRange.sh 
  echo "$script result=$result"
fi


# reset variables
em=""
emline=""
dm=""
line=""
tm=""

# set pcn
pcn=123681

if [[ $result -eq 0 ]]
then # if/then branch
  exec 6<>tm-msg
  read input <&6 && echo "$script time: ${input}" 1>&4
  exec 6<>tm-msg
  script="AccountPeriodBalanceRecreatePeriodRange"
  printf "\nStarting: $script\n" 1>&4
  cd ../AccountPeriodBalanceRecreatePeriodRange
  source AccountPeriodBalanceRecreatePeriodRange.sh 
  echo "$script result=$result"
fi

# reset variables
em=""
emline=""
dm=""
line=""
tm=""

# reset variables
em=""
emline=""
dm=""
line=""
tm=""

# set pcn
pcn=123681

if [[ $result -eq 0 ]]
then # if/then branch
  exec 6<>tm-msg
  read input <&6 && echo "$script time: ${input}" 1>&4
  exec 6<>tm-msg
  script="AccountPeriodBalanceRecreateOpenPeriodRange"
  printf "\nStarting: $script\n" 1>&4
  cd ../AccountPeriodBalanceRecreateOpenPeriodRange
  source AccountPeriodBalanceRecreateOpenPeriodRange.sh 
  echo "$script result=$result"
fi

# reset variables
em=""
emline=""
dm=""
line=""
tm=""
if [[ $result -eq 0 ]] && [[$etl_only -eq 0]]
then # if/then branch
  exec 6<>tm-msg
  read input <&6 && echo "$script time: ${input}" 1>&4
  exec 6<>tm-msg
  script="TrialBalanceExcel"
  printf "\nStarting: $script\n" 1>&4
  cd ../TrialBalanceExcel
  source TrialBalanceExcel.sh 
  echo "$script result=$result"
  echo "TrialBalanceExcel.sh result=$result"
fi 

cd ../PipeLine 

# echo "pwd: $(pwd)"
exec 3<>error-msg
while IFS= read -r emline
do
  em="${em}"$'\n'"${emline}"  
  #  p="${var1}"$'\n'"${var2}"
  # echo "$line"
done <&3
# echo "$script error message=$em"

exec 4<>dbg-msg
while IFS= read -r line
do
  dm="${dm}"$'\n'"${line}"  
  #  p="${var1}"$'\n'"${var2}"
  # echo "$line"
done <&4
# echo "$script debug messages=$dm"

exec 6<>tm-msg
read tm <&6 && echo "$script time: ${tm}" 1>&4
# echo "$script time=$tm"

if [[ $result -ne 0 ]]
then # if/then branch
  printf "\n$pipeline pipeline terminated on $script script.\n$script script failed. \nerror message: $em \ndebug messages: $dm \nlast script time=$tm" 1>&4
  printf "$pipeline pipeline terminated on $script script.\n$script script failed. \nerror message: $em \ndebug messages: $dm \nlast script time=$tm" | mail -s "$pipeline Pipeline Failure" bgroves@buschegroup.com
else
  printf "\n$pipeline pipeline successful all scripts completed." 1>&4
  printf "$pipeline pipeline successful all scripts have completed." | mail -s "$pipeline Pipeline Success" bgroves@buschegroup.com
fi

# # Close FD
# As far as I can see, exec 3>&- and exec 3<&- are the same and 
# can be used on any file descriptor, regardless of how it was opened. 
exec 3>&- 4>&- 5>&- 6>&- 

