#!/usr/bin/bash
# k8s bash location
#!/bin/bash
# ubuntu desktop bash location
#!/usr/bin/bash
# python debug1.py
# ./debug2.sh
# pipeline="TrialBalance"
# https://raw.githubusercontent.com/rogalmic/vscode-bash-debug/gif/images/bash-debug-samp-launch-autoconfig.gif
# Open msg file with FD of 10
exec 10>msg 

printf "\n\$1: $1" 1>&10
printf "\n\$2: $2" 1>&10
printf "\n\$3: $3" 1>&10
printf "\n\$4: $4" 1>&10
printf "\n\$5: $5" 1>&10
# Close FD
exec 10>&- 


export em=""
export emline=""
export dm=""
export line=""
export tm=""sys.
export result=0

export pcn=""
export pcn_list="123681,300758"

export username="mg.odbcalbion"
export password="Mob3xalbion"
export username2="mgadmin"
export password2="WeDontSharePasswords1!"
export username3="root"
export password3="password"
export username4="MGEdonReportsws@plex.com"
export password4="9f45e3d-67ed-"

# pick 1 host
export MYSQL_HOST="moto"
export MYSQL_HOST="reports03"
export MYSQL_HOST="reports13"

export MYSQL_PORT="31008"

# Transfer data to Azure DW flag
export AZURE_DW=0
# export AZURE_DW=1

export script="none"


# export em="none"
# export emline="none"
# export dm="none"
# export line="none"
# export tm="none"
# export result=0 
# get parameters
printf "\nFrom main.sh"
printf "\nall parameters: $@"
printf "\n\$1: $1"

printf "\nbefore mail"
printf "\nusername = $username"
# script="lv2"
# printf "Pipeline terminated on $script script."
#   printf "Pipeline terminated on $script script." | mail -s "MCP Pipeline Failure" bgroves@buschegroup.com


script="lv2"
cd lv2
source lv2.sh 
printf "\nFrom main.sh -> lv2 result=$result"
exit $result

# script="AccountingYearCategoryType"
# cd ../AccountingYearCategoryType
# source AccountingYearCategoryType.sh 
# # echo "AccountingYearCategoryType result=$result"

# # reset variables
# em=""
# emline=""
# dm=""
# line=""
# tm=""

# if [[ $result -eq 0 ]]
# then # if/then branch
#   script="AccountingAccount"
#   cd ../AccountingAccount
#   source AccountingAccount.sh 
# fi

# # reset variables
# em=""
# emline=""
# dm=""
# line=""
# tm=""


# if [[ $result -eq 0 ]]
# then # if/then branch
#   script="AccountingPeriod"
#   cd ../AccountingPeriod
#   source AccountingPeriod.sh 
# fi

# # reset variables
# em=""
# emline=""
# dm=""
# line=""
# tm=""


# if [[ $result -eq 0 ]]
# then # if/then branch
#   script="AccountingPeriodRanges"
#   cd ../AccountingPeriodRanges
#   source AccountingPeriodRanges.sh 
# fi

# # reset variables
# em=""
# emline=""
# dm=""
# line=""
# tm=""

# if [[ $result -eq 0 ]]
# then # if/then branch
#   script="AccountingStartPeriodUpdate"
#   cd ../AccountingStartPeriodUpdate
#   source AccountingStartPeriodUpdate.sh 
# fi


# # reset variables
# em=""
# emline=""
# dm=""
# line=""
# tm=""

# # set pcn
# pcn=123681

# if [[ $result -eq 0 ]]
# then # if/then branch
#   script="AccountingBalanceAppendPeriodRange"
#   cd ../AccountingBalanceAppendPeriodRange
#   source AccountingBalanceAppendPeriodRange.sh 
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

# # reset variables
# em=""
# emline=""
# dm=""
# line=""
# tm=""

# # set pcn
# pcn=123681

# if [[ $result -eq 0 ]]
# then # if/then branch
#   script="AccountActivitySummaryGetOpenPeriodRange"
#   cd ../AccountActivitySummaryGetOpenPeriodRange
#   source AccountActivitySummaryGetOpenPeriodRange.sh 
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
#   script="AccountActivitySummaryGetOpenPeriodRange"
#   cd ../AccountActivitySummaryGetOpenPeriodRange
#   source AccountActivitySummaryGetOpenPeriodRange.sh 
# fi


# # reset variables
# em=""
# emline=""
# dm=""
# line=""
# tm=""

# # set pcn
# pcn=123681

# if [[ $result -eq 0 ]]
# then # if/then branch
#   script="AccountPeriodBalanceRecreatePeriodRange"
#   cd ../AccountPeriodBalanceRecreatePeriodRange
#   source AccountPeriodBalanceRecreatePeriodRange.sh 
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
#   script="AccountPeriodBalanceRecreatePeriodRange"
#   cd ../AccountPeriodBalanceRecreatePeriodRange
#   source AccountPeriodBalanceRecreatePeriodRange.sh 
# fi

# # reset variables
# em=""
# emline=""
# dm=""
# line=""
# tm=""

# # set pcn
# pcn=123681

# if [[ $result -eq 0 ]]
# then # if/then branch
#   script="AccountPeriodBalanceRecreateOpenPeriodRange"
#   cd ../AccountPeriodBalanceRecreateOpenPeriodRange
#   source AccountPeriodBalanceRecreateOpenPeriodRange.sh 
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
#   script="AccountPeriodBalanceRecreateOpenPeriodRange"
#   cd ../AccountPeriodBalanceRecreateOpenPeriodRange
#   source AccountPeriodBalanceRecreateOpenPeriodRange.sh 
# fi

# if [[ $result -ne 0 ]]
# then # if/then branch
#   printf "Pipeline terminated at $script\n"
#   printf "Pipeline terminated on $script script." | mail -s "MCP Pipeline Failure" bgroves@buschegroup.com
# fi
