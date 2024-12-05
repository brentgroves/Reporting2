#!/usr/bin/env python

#!/miniconda/bin/python
#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python
#!/miniconda/bin/python # for docker image
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
  pcn = (sys.argv[1])
  username2 = (sys.argv[2])
  password2 = (sys.argv[3])
  username3 = (sys.argv[4])
  password3 = (sys.argv[5])
  mysql_host = (sys.argv[6])
  mysql_port = (sys.argv[7])
  azure_dw = (sys.argv[8])

#%DEV%pcn = '123681'
#%DEV%username2 = 'mgadmin'
#%DEV%password2 = 'WeDontSharePasswords1!'
#%DEV%username3 = 'root'
#%DEV%password3 = 'password'   
#%DEV%mysql_host = 'reports31'
#%DEV%mysql_port = '30031'
#%DEV%azure_dw = '1'

  # https://geekflare.com/calculate-time-difference-in-python/
  start_time = datetime.now()
  end_time = datetime.now()

  current_time = start_time.strftime("%H:%M:%S")
  print_to_stdout(f"Current Time: {current_time}")

  conn3 = mysql.connector.connect(user=username3, password=password3,
                      host=mysql_host,
                      port=mysql_port,
                      database='Plex')

  cursor3 = conn3.cursor()
  start_period = 0
  end_period = 0
  start_open_period = 0
  end_open_period = 0
  no_update = 9
  # The parameters are needed in the call but the output params are not changed but are in result_args.
  result_args =cursor3.callproc('accounting_get_period_ranges', [pcn,start_period,end_period,start_open_period,end_open_period,no_update])
  # result_args =cursor3.callproc('accounting_balance_get_period_range', [123681,period_start2,period_end2])
  #  https://www.mysqltutorial.org/calling-mysql-stored-procedures-python/
  # start_period = result_args[1] #param 2
  # end_period = result_args[2] #param 3
  # start_open_period = result_args[3] #param 4
  # end_open_period = result_args[4] #param 5
  no_update = result_args[5] #param 6

  if no_update != 1:
    if '1'==azure_dw:

      # https://www.pythonfixing.com/2022/02/fixed-how-to-set-db-connection-timeout.html
      conn2 = pyodbc.connect('DSN=dw;UID='+username2+';PWD='+ password2 + ';DATABASE=mgdw',timeout=30)
      # conn2.timeout = 10
      # conn2.autocommit = True
      cursor2 = conn2.cursor()

      # https://code.google.com/archive/p/pyodbc/wikis/GettingStarted.wiki
      rowcount=cursor2.execute("{call Plex.account_period_balance_delete_period_range (?)}",pcn).rowcount
      # rowcount=cursor2.execute("{call Scratch.account_period_balance_delete_period_range}").rowcount
      # https://github.com/mkleehammer/pyodbc/wiki/Cursor
      # The return value is always the cursor itself:
      print_to_stdout(f"call Plex.account_period_balance_delete_period_range - rowcount={rowcount}")
      print_to_stdout(f"call Plex.account_period_balance_delete_period_range - messages={cursor2.messages}")
      cursor2.commit()

      # https://code.google.com/archive/p/pyodbc/wikis/GettingStarted.wiki
      rowcount=cursor2.execute("{call Plex.account_period_balance_recreate_period_range (?)}",pcn).rowcount
      # https://github.com/mkleehammer/pyodbc/wiki/Cursor
      # The return value is always the cursor itself:
      print_to_stdout(f"call Plex.account_period_balance_recreate_period_range - rowcount={rowcount}")
      print_to_stdout(f"call Plex.account_period_balance_recreate_period_range - messages={cursor2.messages}")
      cursor2.commit()
      cursor2.close()
      # https://github.com/mkleehammer/pyodbc/wiki/Cursor
      # https://github.com/mkleehammer/pyodbc/wiki/Features-beyond-the-DB-API#fast_executemany
      # https://towardsdatascience.com/how-i-made-inserts-into-sql-server-100x-faster-with-pyodbc-5a0b5afdba5
      # https://towardsdatascience.com/how-i-made-inserts-into-sql-server-100x-faster-with-pyodbc-5a0b5afdba5


    # cursor2.callproc('get_laptop', [1, ])
    cursor3.callproc('account_period_balance_delete_period_range', [pcn])
    # rowcount=cursor2.execute(txt.format(dellist = params)).rowcount
    print_to_stdout(f"call Plex.account_period_balance_delete_period_range - rowcount={cursor3.rowcount}")
    # print_to_stdout(f"{txt} - messages={cursor2.messages}")
    conn3.commit()

    cursor3.callproc('account_period_balance_recreate_period_range', [pcn])
    # rowcount=cursor2.execute(txt.format(dellist = params)).rowcount
    print_to_stdout(f"call Plex.account_period_balance_recreate_period_range() - rowcount={cursor3.rowcount}")
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
