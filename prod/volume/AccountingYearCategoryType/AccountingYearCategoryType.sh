#!/bin/bash
# status=$?
# set +e
# set +o pipefail
# ./truncate-logs.sh
# exec 3>error-msg 4>dbg-msg 5>error-num 6>tm-msg 
# printf "AccountingYearCategoryType path= $PATH." | mail -s "AccountingYearCategoryType Path" bgroves@buschegroup.com
# printf "\ntop AccountingYearCategoryType"
# ./AccountingYearCategoryType.py '123681,300758' "$username" "$password"
{
  # printf "\nbefore script-start"
  # pwd
../misc/script-start.py 3 "$username2" "$password2" "$username3" "$password3" "$MYSQL_HOST" "$MYSQL_PORT" "$AZURE_DW" 1>&4 2>&3
  # printf "\nafter script-start"

TIMEFORMAT='%R'; time ./AccountingYearCategoryType.py "$pcn_list" "$username" "$password" "$username2" "$password2" "$username3" "$password3" "$MYSQL_HOST" "$MYSQL_PORT" "$AZURE_DW" 1>&4 2>&3
result=$?
# printf "\nafter AccountingYearCategoryType.py result = $result"

if [[ $result -eq 0 ]]
then # if/then branch
  # printf "\nbefore script-end"
  ../misc/script-end.py 3 0 "$username2" "$password2" "$username3" "$password3" "$MYSQL_HOST" "$MYSQL_PORT" "$AZURE_DW" 1>&4 2>&3
else
  ../misc/script-end.py 3 1 "$username2" "$password2" "$username3" "$password3" "$MYSQL_HOST" "$MYSQL_PORT" "$AZURE_DW" 1>&4 2>&3
fi
} 2>&6 

# exec 3>&- 4>&- 5>&- 6>&- 
# exec 3<error-msg 4<dbg-msg 5<error-num 6<tm-msg 

# exec 3>&- 4>&- 5>&- 6>&- 
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
#   printf "AccountingYearCategoryType script failed. \nerror message: $em \ndebug messages: $dm \ntime=$tm" | mail -s "MCP Script Failure" bgroves@buschegroup.com
# fi


# exec 3>&- 4>&- 5>&- 6>&- 
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
