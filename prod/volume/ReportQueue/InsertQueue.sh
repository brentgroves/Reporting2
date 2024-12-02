#!/bin/bash
# python debug1.py
# ./debug2.sh

./truncate-logs.sh

# https://copyconstruct.medium.com/bash-redirection-fun-with-descriptors-e799ec5a3c16
# Open file descriptor
exec 3<>error-msg 4<>dbg-msg 5>error-num 6<>tm-msg 

printf "\n\$1: $1" 1>&4

export params=$1

# export report_id=1
# export etl_only=1
# export params='{"etl_only":0,"report_name":"daily_metrics","email":"bgroves@buschegroup.com","start_period":202201,"end_period":202207}'


# for k8s debugging
# printf "\nInsertQueue:report_id: $report_id" 1>&4
# printf "\nInsertQueue:etl_only=$etl_only" 1>&4
# printf "\nInsertQueue:parameters: $parameters" 1>&4

# for localhost debuggin
printf "\nInsertQueue:params:$params\n" 


export em=""
export emline=""
export dm=""
export line=""
export tm=""
export result=0

# debug only
# these will be set by the reports-crontab-init container.
export username3='root'
export password3='password'
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

script="InsertQueue"
printf "\nStarting: $script\n" 1>&4
{
TIMEFORMAT='%R'; time ./InsertQueue.py "$params"  1>&4 2>&3
# report_id=1,etl_only=1,params='{"etl_only":0,"report_name":"daily_metrics","email":"bgroves@buschegroup.com","start_period":202201,"end_period":202207}'
result=$?
} 2>&6
echo "$script result=$result"

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
  # printf "\n$pipeline pipeline terminated at $script" 1>&4
  # printf "$pipeline pipeline terminated on $script script." | mail -s "$pipeline Pipeline Failure" bgroves@buschegroup.com
  printf "$pipeline pipeline terminated on $script script.\n$script script failed. \nerror message: $em \ndebug messages: $dm \nlast script time=$tm" | mail -s "$pipeline Pipeline Failure" bgroves@buschegroup.com
  printf "$pipeline pipeline terminated on $script script.\n$script script failed. \nerror message: $em \ndebug messages: $dm \nlast script time=$tm" 

else
  printf "\n$pipeline pipeline successful all scripts completed." 1>&4
  printf "$pipeline pipeline successful all scripts have completed." | mail -s "$pipeline Pipeline Success" bgroves@buschegroup.com
fi

# printf "$pipeline pipeline terminated on $script script.\n$script script failed. \nerror message: $em \ndebug messages: $dm \nlast script time=$tm" | mail -s "$pipeline Pipeline Failure" bgroves@buschegroup.com
# printf "$pipeline pipeline terminated on $script script.\n$script script failed. \nerror message: $em \ndebug messages: $dm \nlast script time=$tm" 

# # Close FD
# As far as I can see, exec 3>&- and exec 3<&- are the same and 
# can be used on any file descriptor, regardless of how it was opened. 
exec 3>&- 4>&- 5>&- 6>&- 

