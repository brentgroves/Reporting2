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

from sqlalchemy import true 

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
  ret = 0
#%PROD%username2 = (sys.argv[1])
#%PROD%password2 = (sys.argv[2])
#%PROD%username3 = (sys.argv[3])
#%PROD%password3 = (sys.argv[4])
#%PROD%mysql_host = (sys.argv[5])
#%PROD%mysql_port = (sys.argv[6])
#%PROD%azure_dw = (sys.argv[7])

  username2 = 'mgadmin' 
  password2 = 'WeDontSharePasswords1!' 
  username3 = 'root'
  password3 = 'password'
  mysql_host = 'reports31'
    # # mysql_host = 'reports13'
  mysql_port = '30031'
  azure_dw = '0'

    # https://geekflare.com/calculate-time-difference-in-python/
  start_time = datetime.now()
  end_time = datetime.now()

  current_time = start_time.strftime("%H:%M:%S")
  print_to_stdout(f"Current Time: {current_time}")

  if '1'==azure_dw:
    # https://www.pythonfixing.com/2022/02/fixed-how-to-set-db-connection-timeout.html
    conn2 = pyodbc.connect('DSN=dw;UID='+username2+';PWD='+ password2 + ';DATABASE=mgdw',timeout=30)
    # conn2.timeout = 10
    # conn2.autocommit = True
    cursor2 = conn2.cursor()
    # https://code.google.com/archive/p/pyodbc/wikis/GettingStarted.wiki
    rowcount=cursor2.execute("{call Plex.accounting_start_period_update}").rowcount

    # https://github.com/mkleehammer/pyodbc/wiki/Cursor
    # The return value is always the cursor itself:
    print_to_stdout(f"call Plex.accounting_start_period_update - rowcount={rowcount}")
    print_to_stdout(f"call Plex.accounting_start_period_update - messages={cursor2.messages}")
    cursor2.commit()
    cursor2.close()
    # https://github.com/mkleehammer/pyodbc/wiki/Cursor
    # https://github.com/mkleehammer/pyodbc/wiki/Features-beyond-the-DB-API#fast_executemany
    # https://towardsdatascience.com/how-i-made-inserts-into-sql-server-100x-faster-with-pyodbc-5a0b5afdba5

    # https://towardsdatascience.com/how-i-made-inserts-into-sql-server-100x-faster-with-pyodbc-5a0b5afdba5


  conn3 = mysql.connector.connect(user=username3, password=password3,
                              host=mysql_host,
                              port=mysql_port,
                              database='Plex')

  cursor3 = conn3.cursor()
  # cursor2.callproc('get_laptop', [1, ])
  cursor3.callproc('accounting_start_period_update', [])
  # rowcount=cursor2.execute(txt.format(dellist = params)).rowcount
  print_to_stdout(f"call Plex.accounting_start_period_update() - rowcount={cursor3.rowcount}")
  # print_to_stdout(f"{txt} - messages={cursor2.messages}")
  conn3.commit()
  cursor3.close()


except pyodbc.Error as ex:
  ret = 1
  error_msg = ex.args[1]
  print_to_stderr(f"error {error_msg}") 
  print_to_stderr(f"error {ex.args}") 

except Error as e:
  ret = 1
  print("Error while connecting to MySQL", e)

except BaseException as error:
  ret = 1
  print('An exception occurred: {}'.format(error))

finally:
  end_time = datetime.now()
  tdelta = end_time - start_time 
  print_to_stdout(f"total time: {tdelta}") 
  # print_to_stdout(f"before the commit")
  if 'conn2' in globals():
    conn2.close()
  if 'conn3' in globals():
    if conn3.is_connected():
      conn3.close()
  sys.exit(ret)
