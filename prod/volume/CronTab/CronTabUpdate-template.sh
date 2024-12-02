#!/bin/bash
# python debug1.py
# ./debug2.sh

./truncate-logs.sh

# https://copyconstruct.medium.com/bash-redirection-fun-with-descriptors-e799ec5a3c16
# Open file descriptor
exec 3<>error-msg 4<>dbg-msg 5>error-num 6<>tm-msg 

# printf "\n\$1: $1" 1>&4

# export params=$1
# printf "\nCronTabUpdate params: $params\n" 

export em=""
export emline=""
export dm=""
export line=""
export tm=""
export result=0

%DEV%export crontab_path=/home/brent/src/Reporting/prod/volume/CronTab
%PROD%export crontab_path=/apps/volume/CronTab

export crontab_filename=$crontab_path'/crontab-reports'
printf "\nCronTabUpdate crontab_filename: $crontab_filename" 

export username3=$(</etc/db-user-pass/username3)
export password3=$(</etc/db-user-pass/password3)
# debug only
# these will be set by the reports-crontab-init container in production.
%DEV%export MYSQL_HOST='%MYSQL_HOST%'
%DEV%export MYSQL_PORT='%MYSQL_PORT%'

script="none"

export em=""
export emline=""
export dm=""
export line=""
export tm=""
export result=0 

script="CronTabUpdate"
printf "\nStarting: $script\n" 1>&4
{
TIMEFORMAT='%R'; time ./CronTabUpdate.py 1>&4 2>&3
result=$?
} 2>&6
echo "$script result=$result"


if [[ $result -eq 0 ]]
then # if/then branch
  $(crontab "$crontab_filename") 
fi

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

