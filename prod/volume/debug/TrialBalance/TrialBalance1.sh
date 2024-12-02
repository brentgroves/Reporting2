#!/bin/bash
# status=$?
# https://stackoverflow.com/questions/786376/how-do-i-run-a-program-with-a-different-working-directory-from-current-from-lin
# exec will end the TrialBalance.sh script 
# (cd ./AccountingYearCategoryType && exec python ./exit-num.py 1
# )
# if counting on shebang you need to know which dir python is installed
# (cd ./AccountingYearCategoryType && ./exit-num.py 1)


AccountingYearCategoryType()
{
  (cd ./AccountingYearCategoryType && python ./exit-num.py $1)
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
  echo "AccountingYearCategoryType failed" | mail -s "MCP Script Failure" bgroves@buschegroup.com
  exit 1
fi

AccountingAccount $2
ret=$?
if [[ $ret -eq 0 ]]
then # if/then branch
  echo 'AccountingAccount success'
else # else branch
  echo 'AccountingAccount fail'
  echo "AccountingAccount failed" | mail -s "MCP Script Failure" bgroves@buschegroup.com
  exit 1
fi

exit 0