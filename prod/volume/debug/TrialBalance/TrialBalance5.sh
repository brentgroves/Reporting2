#!/bin/bash
# status=$?
# https://stackoverflow.com/questions/786376/how-do-i-run-a-program-with-a-different-working-directory-from-current-from-lin
# exec will end the TrialBalance.sh script 
# (cd ./AccountingYearCategoryType && exec python ./exit-num.py 1
# )
# if counting on shebang you need to know which dir python is installed
# (cd ./AccountingYearCategoryType && ./exit-num.py 1)
#  { /usr/bin/time -f "%e" ./TrialBalance.sh 0 0 1>/dev/null} | ({read foo; echo hello $foo })
# { /usr/bin/time -f "%e" ./TrialBalance.sh 0 0 1>/dev/null} |& ({read foo; python LogTime.sh $foo } )


AccountingYearCategoryType()
{
  (cd ./AccountingYearCategoryType && python ./AccountingYearCategoryType.py $1 )
  # (cd ./AccountingYearCategoryType && python ./exit-num.py $1)
  # (cd ./AccountingYearCategoryType && python ./exit-num.py $1)
  # time -p (cd ./AccountingYearCategoryType && python ./exit-num.py $1)
  # python ./AccountingYearCategoryType.py
  # python ./AccountingYearCategoryType/AccountingYearCategoryType.py
  # (cd ./AccountingYearCategoryType && python ./AccountingYearCategoryType.py $1 )
  status=$?
  # if [[ $status -eq 0 ]]
  # then # if/then branch
  #   # echo 'success'
  #   return 0
  # else # else branch
  #   # echo 'fail'
  #   return 1
  # fi
  if [[ $status -eq 0 ]]
  then # if/then branch
    # echo 'success'
    return 0
  fi
  if [[ $status -eq 1 ]]
  then # if/then branch
    # echo 'fail'
    return 1
  fi
  if [[ $status -eq 2 ]]
  then # if/then branch
    # echo 'fail'
    return 2
  fi
  if [[ $status -eq 3 ]]
  then # if/then branch
    # echo 'fail'
    return 3
  fi
}

AccountingAccount()
{
  (cd ./AccountingAccount && python ./exit-num.py $1)
  status=$?
  if [[ $status -eq 0 ]]
  then # if/then branch
    # echo 'success'
    return 0
  else # else branch
    # echo 'fail'
    return 1
  fi
}

AccountingYearCategoryType $1
ret=$?
if [[ $ret -eq 0 ]]
then # if/then branch
  echo 'AccountingYearCategoryType success'
else # else branch
  echo 'AccountingYearCategoryType fail'
  echo $ret
  echo "AccountingYearCategoryType failed" | mail -s "MCP Script Failure" bgroves@buschegroup.com
  exit 1
fi

# AccountingAccount $2
# ret=$?
# MY_MESSAGE="Hello World"
# echo $MY_MESSAGE
# if [[ $ret -eq 0 ]]
# then # if/then branch
#   echo 'AccountingAccount success'
# else # else branch
#   echo 'AccountingAccount fail'

#   echo '$ret after return'
#   echo "AccountingAccount failed" | mail -s "MCP Script Failure" bgroves@buschegroup.com
#   exit 1
# fi

exit 0

