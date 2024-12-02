#!/bin/bash
# status=$?
set +e
set +o pipefail

# Begin development section
# Only run this in development platform. Production platform should have all the python modules installed already.
eval "$(conda shell.bash hook)"
conda activate etl
# End development section

python ./AccountingYearCategoryType.py
status=$?
if [[ $status -eq 1 ]]
then # if/then branch
  echo "AccountingYearCategoryType failed" | mail -s "MCP Script Failure" bgroves@buschegroup.com
  AccountingYearCategoryTypeError=1 
  # echo 'fail'
fi

# echo "AccountingYearCategoryType failed" | mail -s "MCP Script Failure" bgroves@buschegroup.com
