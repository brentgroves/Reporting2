#!/usr/bin/env python

#!/miniconda/bin/python # for docker image
#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python # for debugging
# https://docs.python-zeep.org/en/master/

import pyodbc 
from datetime import datetime
import sys 
import mysql.connector
from mysql.connector import Error

import os
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

try:
  script_key = (sys.argv[1])
  username = (sys.argv[2])
  password = (sys.argv[3])
  username2 = (sys.argv[4])
  password2 = (sys.argv[5])
  mysql_host = (sys.argv[6])
  mysql_port = (sys.argv[7])
  azure_dw = (sys.argv[8])

#%DEV%script_key = '4'
#%DEV%username = 'mgadmin'
#%DEV%password = 'WeDontSharePasswords1!'
#%DEV%username2 = 'root'
#%DEV%password2 = 'password'    # print(f"params={params}")
#%DEV%mysql_host = 'reports31'
#%DEV%mysql_port = '30031'
#%DEV%azure_dw = '1'

  ret = 0
  # https://geekflare.com/calculate-time-difference-in-python/
  start_time = datetime.now()
  end_time = datetime.now()

  current_time = start_time.strftime("%H:%M:%S")
  print_to_stdout(f"{current_time=}")

  if '1'==azure_dw:
    # https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-1-configure-development-environment-for-pyodbc-python-development?view=sql-server-ver15
    conn = pyodbc.connect('DSN=dw;UID='+username+';PWD='+ password + ';DATABASE=mgdw')

    # https://stackoverflow.com/questions/11451101/retrieving-data-from-sql-using-pyodbc
    cursor = conn.cursor()
    cursor.execute("{call ETL.script_start (?)}", script_key)
    cursor.commit()
    cursor.close()
    
  conn2 = mysql.connector.connect(user=username2, password=password2,
                          host=mysql_host,
                          port=mysql_port,
                          database='ETL')
  cursor2 = conn2.cursor()
  # cursor2.callproc('get_laptop', [1, ])
  cursor2.callproc('script_start', [script_key])
  # https://mysqlcode.com/call-mysql-stored-procedure-in-python/
  # cursor2.callproc('ETL.script_start', ["1"])
  # cursor2.execute("{call ETL.script_start (?)}", script_key)
  conn2.commit()
  cursor2.close()

except pyodbc.Error as ex:
  ret = 1
  error_msg = ex.args[1]
  print_to_stderr(error_msg) 

except Error as e:
  ret = 1
  print("MySQL error: ", e)

except BaseException as error:
  ret = 1
  print('An exception occurred: {}'.format(error))

finally:
  end_time = datetime.now()
  tdelta = end_time - start_time 
  print_to_stdout(f"total time: {tdelta}") 
  if 'conn' in globals():
    conn.close()
  if 'conn2' in globals():
    if conn2.is_connected():
      conn2.close()
  sys.exit(ret)
