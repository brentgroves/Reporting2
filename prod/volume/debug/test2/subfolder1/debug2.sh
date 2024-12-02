#!/bin/bash
# python debug1.py

python ./AccountingYearCategoryType.py

status=$?
if [[ $status -eq 1 ]]
then # if/then branch
  echo "AccountingYearCategoryType failed" | mail -s "MCP Script Failure" bgroves@buschegroup.com
  AccountingYearCategoryTypeError=1 
  # echo 'fail'
fi
