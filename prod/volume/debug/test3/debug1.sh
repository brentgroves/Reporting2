#!/bin/bash
# python debug1.py
# ./debug2.sh
export result=0 
# exec 3>error-msg 4>dbg-msg 5>error-num 6>tm-msg 7>final
# exec 3>result
cd subfolder1
source debug2.sh 
echo "script1 result=$result"

cd ../subfolder2
source debug2.sh 
echo "script2 result=$result"


# sends err to file and time to $var
# ( cd ./subfolder1; source ./debug2.sh \
#   echo "[A] AccountingYearCategoryTypeError is: $AccountingYearCategoryTypeError" 1>&3 ; 
# );
# exec 3>&-

# exec 3<AccountingYearCategoryTypeResult
# read -r result <&3       # read the first 3 characters from fd 5.
# echo "result=$result" 
# echo "AccountingYearCategoryTypeResult=$result"

