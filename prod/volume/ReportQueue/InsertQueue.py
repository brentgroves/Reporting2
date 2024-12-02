#!/usr/bin/env python

#!/miniconda/bin/python
#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python
#!/miniconda/bin/python # for docker image
#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python # for debugging
# https://docs.python-zeep.org/en/master/
import pyodbc 
from datetime import datetime
import sys 
import mysql.connector
from mysql.connector import Error
import os
import json 


sys.path.insert(1, '/home/brent/src/Reporting/prod/etl/modules')   
import report_queue

# https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver16
# https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/programming-guidelines?view=sql-server-ver16
# remember to source oaodbc64.sh to set env variables.
# https://github.com/mkleehammer/pyodbc/wiki/Calling-Stored-Procedures
# https://thepythonguru.com/fetching-records-using-fetchone-and-fetchmany/
# https://code.google.com/archive/p/pyodbc/wikis/Cursor.wiki
def print_to_stdout(*a):
    # Here a is the array holding the objects
    # passed as the argument of the function
    print(os.path.basename(__file__)+':',*a, file = sys.stdout)


def print_to_stderr(*a):
    # Here a is the array holding the objects
    # passed as the argument of the function
    print(os.path.basename(__file__)+':',*a, file = sys.stderr)

def insert_queue(params):
  ret = 0
  # sys.exit(0)
  print_to_stdout(f'params={params}')
  report_queue.insert_queue(params=params)
  return
  
if __name__ == '__main__':
  print(f"start of InsertQueue.py")
  print('Number of arguments:', len(sys.argv), 'arguments.')
  print('Argument List:', str(sys.argv))
  print(f'arg[1]={str(sys.argv[1])}')
  params=str(sys.argv[1])
  insert_queue(params=params)
# insert_queue(report_id=report_id,etl_only=etl_only,params='{"etl_only":0,"report_name":"daily_metrics","email":"bgroves@buschegroup.com","start_period":202201,"end_period":202207}')
