./truncate-logs.sh
exec 3>error-msg 4>dbg-msg 5>error-num 6>tm-msg 
# printf "AccountingYearCategoryType path= $PATH." | mail -s "AccountingYearCategoryType Path" bgroves@buschegroup.com

# ./AccountingYearCategoryType.py '123681,300758' "$username" "$password"
{
../misc/script-start.py 3
} 2>&6 
