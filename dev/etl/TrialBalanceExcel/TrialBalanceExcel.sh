#!/bin/bash
# status=$?
# set +e
# set +o pipefail

./truncate-logs.sh

exec 3>error-msg 4>dbg-msg 5>error-num 6>tm-msg 
# exec 7>error-msg 8>dbg-msg 9>error-num 10>tm-msg 

{
# pwd 
# ls -al ../misc/dw-script-start.py
# TIMEFORMAT='%R';time echo "123" 1>&4 
../misc/dw-script-start.py 11 "$username3" "$password3" "$MYSQL_HOST" "$MYSQL_PORT" 
TIMEFORMAT='%R';time ./TrialBalanceExcel.py "$pcn" "$username3" "$password3" "$MYSQL_HOST" "$MYSQL_PORT" "$start_period" "$end_period" 1>&4 2>&3
result=$?
if [[ $result -eq 0 ]]
then # if/then branch
    ../misc/dw-script-end.py 11 0 "$username3" "$password3" "$MYSQL_HOST" "$MYSQL_PORT"
else
  ../misc/dw-script-end.py 11 1 "$username3" "$password3" "$MYSQL_HOST" "$MYSQL_PORT"
fi
} 2>&6 

exec 3>&- 4>&- 5>&- 6>&- 
# exec 7>&- 8>&- 9>&- 10>&- 
exec 3<error-msg 4<dbg-msg 5<error-num 6<tm-msg 
# exec 7<error-msg 8<dbg-msg 9<error-num 10<tm-msg 

read -r tm <&6       # read the first 3 characters from fd 5.
echo "\ntime=$tm" 


while IFS= read -r emline
do
  em="${em}"$'\n'"${emline}"  
  #  p="${var1}"$'\n'"${var2}"
  # echo "$line"
done <&3
echo "em = $em"

while IFS= read -r line
do
  dm="${dm}"$'\n'"${line}"  
  #  p="${var1}"$'\n'"${var2}"
  # echo "$line"
done <&4
echo "dm = $dm"

echo "result=$result"

if [[ $result -ne 0 ]]
then # if/then branch
  printf "TrialBalanceExcel($pcn) script failed. \nerror message: $em \ndebug messages: $dm \ntime=$tm" | mail -s "MCP Script Failure" bgroves@buschegroup.com
fi


exec 3>&- 4>&- 5>&- 6>&- 
# exec 3<error-msg 4<dbg-msg 5<error-num 6<tm-msg 
# read -r tm <&6       # read the first 3 characters from fd 5.
# echo "time=$tm" 

# exec 3<>error-msg 4<>dbg-msg 5<>error-num 6<>tm-msg 7<>final

# # Begin development section
# # Only run this in development platform. Production platform should have all the python modules installed already.
# # eval "$(conda shell.bash hook)"
# # conda activate etl
# # End development section

# python ./AccountingYearCategoryType.py
# status=$?
# if [[ $status -eq 1 ]]
# then # if/then branch
#   echo "AccountingYearCategoryType failed" | mail -s "MCP Script Failure" bgroves@buschegroup.com
#   AccountingYearCategoryTypeError=1 
#   # echo 'fail'
# fi

# echo "AccountingYearCategoryType failed" | mail -s "MCP Script Failure" bgroves@buschegroup.com
