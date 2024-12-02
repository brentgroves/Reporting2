
import sys

arg1 = sys.argv[1]
 # convert the arg1 to an int or sys.exit(status) will return a string
status = int(arg1)
 
# print("status") 

if status != 0:
    # exits the program
    sys.exit(status)    
else:
    sys.exit(0)    
#!python
