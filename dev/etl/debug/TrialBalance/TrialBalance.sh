#!/bin/bash
# status=$?
set +e
set +o pipefail

AccountingYearCategoryType()
{
  # var=$( TIMEFORMAT='%R'; { time source ./TrialBalance.sh 1>/dev/null; } 2>&1  )

  (cd ./AccountingYearCategoryType && python ./AccountingYearCategoryType.py )
  status=$?
  # echo stat $status
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


AccountingYearCategoryType 
ret=$?
if [[ $ret -eq 0 ]]
then # if/then branch
  echo 'AccountingYearCategoryType success'
else # else branch
  # AccountingYearCategoryTypeError=1
  AccountingYearCategoryTypeError=1 
  echo $ret
  echo "AccountingYearCategoryType failed" | mail -s "MCP Script Failure" bgroves@buschegroup.com
  # exit 0
fi

# { /usr/bin/time -f "%e" ./TrialBalance.sh 0 0 1>/dev/null} |& ({read foo; python LogTime.sh $foo } )