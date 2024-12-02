#!/bin/bash
{ /usr/bin/time -f "%e" ./TrialBalance.sh 0 0 1>/dev/null } |& read foo; python LogTime.sh $foo
# (cd ./TrialBalance && { /usr/bin/time -f "%e" ./TrialBalance/TrialBalance.sh 0 0 1>/dev/null} |& ({read foo; python LogTime.sh $foo } ) )
# { /usr/bin/time -f "%e" ./TrialBalance/TrialBalance.sh 0 0 1>/dev/null} |& ({read foo; python LogTime.sh $foo } ) 
# (cd ./TrialBalance && python ./TrialBalance.sh )