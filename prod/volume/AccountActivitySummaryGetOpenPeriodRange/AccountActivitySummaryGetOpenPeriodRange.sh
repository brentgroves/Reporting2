#!/bin/bash
# status=$?
# set +e
# set +o pipefail

# ./truncate-logs.sh

# exec 3>error-msg 4>dbg-msg 5>error-num 6>tm-msg 
# exec 7>error-msg 8>dbg-msg 9>error-num 10>tm-msg 
printf "\nline:10" 

{
../misc/script-start.py 7 "$username2" "$password2" "$username3" "$password3" "$MYSQL_HOST" "$MYSQL_PORT" "$AZURE_DW" 1>&4 2>&3
printf "\nline:14" 

# TIMEFORMAT='%R'; time ./AccountActivitySummaryGetOpenPeriodRange.py "$pcn" "$username2" "$password2" "$username3" "$password3" "$username4" "$password4" "$MYSQL_HOST" "$MYSQL_PORT" "$AZURE_DW" 1>&4 2>&3
TIMEFORMAT='%R'; time ./TEST.py "$pcn" "$username2" "$password2" "$username3" "$password3" "$username4" "$password4" "$MYSQL_HOST" "$MYSQL_PORT" "$AZURE_DW" 1>&4 2>&3
printf "\nline:18"
# TIMEFORMAT='%R'; time ./AccountingAccount.py '123681,300758,310507,306766,300757' 1>&8 2>&7
result=$?
if [[ $result -eq 0 ]]
then # if/then branch
  ../misc/script-end.py 7 0 "$username2" "$password2" "$username3" "$password3" "$MYSQL_HOST" "$MYSQL_PORT" "$AZURE_DW" 1>&4 2>&3
else
  ../misc/script-end.py 7 1 "$username2" "$password2" "$username3" "$password3" "$MYSQL_HOST" "$MYSQL_PORT" "$AZURE_DW" 1>&4 2>&3
fi
} 2>&6 

# exec 3>&- 4>&- 5>&- 6>&- 
# # exec 7>&- 8>&- 9>&- 10>&- 
# exec 3<error-msg 4<dbg-msg 5<error-num 6<tm-msg 
# # exec 7<error-msg 8<dbg-msg 9<error-num 10<tm-msg 

# read -r tm <&6       # read the first 3 characters from fd 5.
# echo "time=$tm" 


# while IFS= read -r emline
# do
#   em="${em}"$'\n'"${emline}"  
#   #  p="${var1}"$'\n'"${var2}"
#   # echo "$line"
# done <&3
# echo "em = $em"

# while IFS= read -r line
# do
#   dm="${dm}"$'\n'"${line}"  
#   #  p="${var1}"$'\n'"${var2}"
#   # echo "$line"
# done <&4
# echo "dm = $dm"

# echo "result=$result"

# if [[ $result -ne 0 ]]
# then # if/then branch
#   printf "AccountActivitySummaryGetOpenPeriodRange($pcn) script failed. \nerror message: $em \ndebug messages: $dm \ntime=$tm" | mail -s "MCP Script Failure" bgroves@buschegroup.com
# fi


# exec 3>&- 4>&- 5>&- 6>&- 
