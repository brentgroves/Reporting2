#!/bin/bash
## test-pipeline-standard
## version 0.0.1 - initial
#!python
import sys

print(f"Name of the script      : {sys.argv[0]=}")
print(f"Arguments of the script : {sys.argv[1:]=}")
print('hello from python file.')

#  { /usr/bin/time -f "%e" ./TrialBalance.sh 0 0 1>/dev/null} | ({read foo; echo hello $foo })
