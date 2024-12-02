#!/bin/bash
# python debug1.py
# ./debug2.sh

./truncate-logs.sh

# Open file descriptor
exec 4>dbg-msg 

printf "\n\$1: $1" 1>&4
printf "\n\$2: $2" 1>&4
printf "\n\$3: $3" 1>&4
printf "\n\$4: $4" 1>&4
printf "\n\$5: $5" 1>&4

export report_name=$1
export email=$2
export start_period=$3
export end_period=$4
export frequency=$5

# for k8s debugging
printf "\nreport_name: $report_name" 1>&4
printf "\nemail: $email" 1>&4
printf "\nstart_period: $start_period" 1>&4
printf "\nend_period: $end_period" 1>&4
printf "\nfrequency: $frequency" 1>&4

# for localhost debuggin
printf "\nreport_name: $report_name" 
printf "\nemail: $email" 
printf "\nstart_period: $start_period" 
printf "\nend_period: $end_period" 
printf "\nfrequency: $frequency\n" 

# Close file descriptor before source command.
# I don't believe the file descriptors survive a source command
exec 4>&-  

pipeline="TrialBalance"
export em=""
export emline=""
export dm=""
export line=""
export tm=""
export result=0

export pcn=""
export pcn_list="123681,300758"

# export username=$(</etc/foo/username)
# export password=$(</etc/foo/password)
# export username2=$(</etc/foo/username2)
# export password2=$(</etc/foo/password2)
# export username3=$(</etc/foo/username3)
# export password3=$(</etc/foo/password3)
# export username4=$(</etc/foo/username4)
# export password4=$(</etc/foo/password4)
# export MYSQL_HOST=$(</etc/foo/MYSQL_HOST)
# export MYSQL_PORT=$(</etc/foo/MYSQL_PORT)
# export AZURE_DW=$(</etc/foo/AZURE_DW)

export username='mg.odbcalbion'
export password='Mob3xalbion'
export username2='mgadmin'
export password2='WeDontSharePasswords1!'
export username3='root'
export password3='password'
export username4='MGEdonReportsws@plex.com'
export password4='9f45e3d-67ed-'
export MYSQL_HOST='reports13'
export MYSQL_PORT='31008'
export AZURE_DW='0'

script="none"


export em="none"
export emline="none"
export dm="none"
export line="none"
export tm="none"
export result=0 

# The source command reads and executes commands from the file 
# specified as its argument in the current shell environment. 
# It is useful to load functions, 
# variables, and configuration files into shell scripts.

script="AccountingYearCategoryType"
cd ../AccountingYearCategoryType
source AccountingYearCategoryType.sh 
echo "AccountingYearCategoryType result=$result"

# reset variables
em=""
emline=""
dm=""
line=""
tm=""

if [[ $result -eq 0 ]]
then # if/then branch
  script="AccountingAccount"
  cd ../AccountingAccount
  source AccountingAccount.sh 
fi

# reset variables
em=""
emline=""
dm=""
line=""
tm=""

if [[ $result -eq 0 ]]
then # if/then branch
  script="AccountingPeriod"
  cd ../AccountingPeriod
  source AccountingPeriod.sh 
fi

# reset variables
em=""
emline=""
dm=""
line=""
tm=""

if [[ $result -eq 0 ]]
then # if/then branch
  script="AccountingPeriodRanges"
  cd ../AccountingPeriodRanges
  source AccountingPeriodRanges.sh 
fi

# reset variables
em=""
emline=""
dm=""
line=""
tm=""

if [[ $result -eq 0 ]]
then # if/then branch
  script="AccountingStartPeriodUpdate"
  cd ../AccountingStartPeriodUpdate
  source AccountingStartPeriodUpdate.sh 
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
  script="AccountingBalanceAppendPeriodRange"
  cd ../AccountingBalanceAppendPeriodRange
  source AccountingBalanceAppendPeriodRange.sh 
fi

# reset variables
em=""
emline=""
dm=""
line=""
tm=""

# set pcn
pcn=300758
if [[ $result -eq 0 ]]
then # if/then branch
  script="AccountingBalanceAppendPeriodRange"
  cd ../AccountingBalanceAppendPeriodRange
  source AccountingBalanceAppendPeriodRange.sh 
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
  script="AccountActivitySummaryGetOpenPeriodRange"
  cd ../AccountActivitySummaryGetOpenPeriodRange
  source AccountActivitySummaryGetOpenPeriodRange.sh 
fi

# reset variables
em=""
emline=""
dm=""
line=""
tm=""

# set pcn
pcn=300758

if [[ $result -eq 0 ]]
then # if/then branch
  script="AccountActivitySummaryGetOpenPeriodRange"
  cd ../AccountActivitySummaryGetOpenPeriodRange
  source AccountActivitySummaryGetOpenPeriodRange.sh 
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
  script="AccountPeriodBalanceRecreatePeriodRange"
  cd ../AccountPeriodBalanceRecreatePeriodRange
  source AccountPeriodBalanceRecreatePeriodRange.sh 
fi

# reset variables
em=""
emline=""
dm=""
line=""
tm=""

# set pcn
pcn=300758

if [[ $result -eq 0 ]]
then # if/then branch
  script="AccountPeriodBalanceRecreatePeriodRange"
  cd ../AccountPeriodBalanceRecreatePeriodRange
  source AccountPeriodBalanceRecreatePeriodRange.sh 
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
  script="AccountPeriodBalanceRecreateOpenPeriodRange"
  cd ../AccountPeriodBalanceRecreateOpenPeriodRange
  source AccountPeriodBalanceRecreateOpenPeriodRange.sh 
fi

# reset variables
em=""
emline=""
dm=""
line=""
tm=""

# set pcn
pcn=300758

if [[ $result -eq 0 ]]
then # if/then branch
  script="AccountPeriodBalanceRecreateOpenPeriodRange"
  cd ../AccountPeriodBalanceRecreateOpenPeriodRange
  source AccountPeriodBalanceRecreateOpenPeriodRange.sh 
fi

# reset variables
em=""
emline=""
dm=""
line=""
tm=""

if [[ $result -eq 0 ]]
then # if/then branch
  script="TrialBalanceExcel"
  cd ../TrialBalanceExcel
  source TrialBalanceExcel.sh 
  echo "TrialBalanceExcel.sh result=$result"
fi 

# Open file descriptor
exec 4>dbg-msg 

if [[ $result -ne 0 ]]
then # if/then branch
  printf "\nPipeline terminated at $script" 1>&4
  printf "Pipeline terminated on $script script." | mail -s "MCP Pipeline Failure" bgroves@buschegroup.com
else
  printf "\nPipeline Successful all scripts completed." 1>&4
  printf "Pipeline successful all scripts have completed." | mail -s "MCP Pipeline Success" bgroves@buschegroup.com
fi

# Close FD
exec 4>&- 
