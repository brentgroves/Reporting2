#!/bin/bash
# The set -e option instructs bash to immediately exit if any command [1] has a non-zero exit status.
# set -e
set +e
# Affects variables. When set, a reference to any variable you haven't previously defined - with the exceptions of @ - is an error, and causes the program to immediately exit.
# set -u
# This setting prevents errors in a pipeline from being masked. If any command in a pipeline fails, that return code will be used as the return code of the whole pipeline. By default, the pipeline's return code is that of the last command even if it succeeds.
# set -o pipefail
set +o pipefail
# Enables a mode of the shell where all executed commands are printed to the terminal.
# set -x
# The IFS variable - which stands for Internal Field Separator - controls what Bash calls word splitting.
# IFS=$' '
# IFS=$'\n'

# export AccountingYearCategoryTypeError=0 
# . ./TrialBalance.sh
# echo "The message is: $AccountingYearCategoryTypeError"

# https://stackoverflow.com/questions/9772036/pass-all-variables-from-one-shell-script-to-another
# /usr/bin/time -f 'real %e' -o OUTPUT_FILE ./TrialBalance.sh 0 0 > /dev/null 2> /dev/null
# /usr/bin/time -f 'real %e' -o OUTPUT_FILE ls > /dev/null 2> /dev/null
# REALTIME=$(cat OUTPUT_FILE | cut -f 2 -d ' ')
# echo "real time is $REALTIME"
# export time1=$( { /usr/bin/time -f "%e" ./TrialBalance.sh 0 0 1>/dev/null; } 2>&1 ) # works from script
# echo "hello $time1" 
# printenv time2
# https://stackoverflow.com/questions/26784870/parsing-the-output-of-bashs-time-builtin
export AccountingYearCategoryTypeError=0 
export MESSAGE="hello"

# . ./TrialBalance.sh
# var=$( TIMEFORMAT='%R'; { time source ./TrialBalance.sh 1>/dev/null; echo "[A] AccountingYearCategoryTypeError is: $AccountingYearCategoryTypeError" ; } 2>&1  )
var=$( cd ./AccountingYearCategoryType; TIMEFORMAT='%R'; \
{ time source ./AccountingYearCategoryType.sh 1>/dev/null; \
  echo "[A] AccountingYearCategoryTypeError is: $AccountingYearCategoryTypeError" ; 
} 2>&1  )
# var=$( cd ./AccountingYearCategoryType; TIMEFORMAT='%R'; { time source ls ; } 2>&1 )
# var=$( cd ./AccountingYearCategoryType; TIMEFORMAT='%R'; { time source python ./AccountingYearCategoryType.py 1>/dev/null ; } 2>&1 )

# var=$( TIMEFORMAT='%R'; { time source ./TrialBalance.sh 1>/dev/null; } 2>&1  )
# var=$(TIMEFORMAT='%R'; { time ls; } 2>&1)
# /usr/bin/time -f "%e" source ./TrialBalance.sh 0 0 1>/dev/null;  # works from script
echo "var is: $var"
# time source ./TrialBalance.sh 0 0 1>/dev/null;  # works from script
# { /usr/bin/time -f "%e" source ./TrialBalance.sh 0 0 1>/dev/null; } # works from script
# echo "AccountingYearCategoryTypeError is: $AccountingYearCategoryTypeError"
# MESSAGE="goodbye"; 
echo "[A] AccountingYearCategoryTypeError is: $AccountingYearCategoryTypeError"

# { /usr/bin/time -f "%e" ./TrialBalance.sh 0 0 1>/dev/null; } |& read foo; python LogTime.py $foo # works from command line
# { /usr/bin/time -f "%e" ./TrialBalance.sh 0 0 1>/dev/null; } |& read foo; python LogTime.py $foo # dont work in script
# { /usr/bin/time -f "%e" ./TrialBalance.sh 0 0 1>/dev/null; } |& read foo; python LogTime.py $foo # dont work in script

# { /usr/bin/time -f "%e" ./TrialBalance.sh 0 0 ; } 1>/dev/null |& read foo ; python LogTime.py $foo # dont work 
# { /usr/bin/time -f "%e" ./TrialBalance.sh 0 0 1>/dev/null; } |& read foo; python LogTime.py $foo 
# ( { /usr/bin/time -f "%e" ./TrialBalance.sh 0 0 1>/dev/null; } |& read foo; python LogTime.py $foo )
# (cd ./TrialBalance && python ./TrialBalance.sh )

# export time=$( { /usr/bin/time -f "%e" ls; } 2>&1 )    # note the curly braces

# exec 3>&1 4>&2
# export time1=$( { /usr/bin/time -f "%e" ls 1>/dev/null; } 2>&1)
# export time1=$( { /usr/bin/time -f "%e" ls 1>&3 2>&4; } 2>&1)
# exec 3>&- 4>&-
# printenv time1

# captures the time only, passes stdout through
# exec 3>&1 4>&2
# export time=$( { /usr/bin/time -f "%e" ls 1>&3 2>&4; } 2>&1)
# exec 3>&- 4>&-
# printenv time

# @Sirex: Streams 3 and 4 are streams created by the exec command in my answer using available file descriptors. 
# Any available file descriptors could be used. Streams 3 and 4 are copies of 1 (stdout) and 2 (stderr), respectively. 
# This allows the output of ls to pass normally to stdout and stderr via 3 and 4 while the output of time 
# (which normally goes to stderr) is redirected to the original stdout (1) and then captured in the variable using 
# command substitution. As you can see in my example, the filenames bar and baz are output to the terminal. ...