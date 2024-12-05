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
%PROD%pcn_list = (sys.argv[1])
%PROD%username = (sys.argv[2])
%PROD%password = (sys.argv[3])
%PROD%username2 = (sys.argv[4])
%PROD%password2 = (sys.argv[5])
%PROD%username3 = (sys.argv[6])
%PROD%password3 = (sys.argv[7])
%PROD%mysql_host = (sys.argv[8])
%PROD%mysql_port = (sys.argv[9])
%PROD%azure_dw = (sys.argv[10])

%DEV%pcn_list = '123681'
# %DEV%pcn_list = '123681,300758'
    # # pcn_list = '123681,300758,310507,306766,300757'
%DEV%username = 'mg.odbcalbion'
%DEV%password = 'Mob3xalbion'
%DEV%username2 = 'mgadmin'
%DEV%password2 = 'WeDontSharePasswords1!'
%DEV%username3 = 'root'
%DEV%password3 = 'password'
%DEV%mysql_host = '%MYSQL_HOST%'
    # # mysql_host = 'reports13'
%DEV%mysql_port = '%MYSQL_PORT%'
%DEV%azure_dw = '%AZURE_DW%'

    # https://geekflare.com/calculate-time-difference-in-python/
  start_time = datetime.now()
  end_time = datetime.now()

  current_time = start_time.strftime("%H:%M:%S")
  print_to_stdout(f"Current Time: {current_time}")

  # https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-1-configure-development-environment-for-pyodbc-python-development?view=sql-server-ver15
  # password = 'wrong' 
  conn = pyodbc.connect('DSN=Plex;UID='+username+';PWD='+ password)
  # https://stackoverflow.com/questions/11451101/retrieving-data-from-sql-using-pyodbc
  cursor = conn.cursor()
    
  # accounting_period_dw_import
  cursor.execute("{call sproc300758_11728751_2059406 (?)}", pcn_list)
  rows = cursor.fetchall()
  cursor.close()
  fetch_time = datetime.now()
  tdelta = fetch_time - start_time 
  print_to_stdout(f"fetch_time={tdelta}") 

  length = len(rows)
  i = 0
  print(f"length={length}")
  f = '%Y-%m-%d %H:%M:%S.%f'
  # Convert Plex format to datetime with 3 precision second decimal
  # If DW column was datetime2 no conversion would be necessary
  while i < length:
    if(rows[i][9] is not None):
      r9=rows[i][9]
      # print(f"period_key={rows[i][1]}len={len(r9)},r9={r9}")
      if(len(r9)==19):
        ts=r9+'.000'
      else:        
        ts=r9[:-6]
      # print(f"len={len(ts)},ts={ts}")
      rows[i][9]=ts
            # dt=datetime.strptime(ts, f)
            # et=dt.strftime("%f")[:-3]
            # st=dt.strftime("%Y-%m-%d %H:%M:%S")
            # rows[i][9]=st+'.'+et
            # print(f"i={i},st={st},et={et}")
    i += 1

  conn2 = pyodbc.connect('DSN=dw;UID='+username2+';PWD='+ password2 + ';DATABASE=mgdw')

  cursor2 = conn2.cursor()
      # https://code.google.com/archive/p/pyodbc/wikis/GettingStarted.wiki
      # delete the previous runs values
  del_command = f"delete from Plex.accounting_period where pcn in ({pcn_list}) and ordinal = 0"
      # del_command = f"delete from Scratch.accounting_period where pcn in ({params})"

      # https://github.com/mkleehammer/pyodbc/wiki/Cursor
      # The return value is always the cursor itself:
  rowcount=cursor2.execute(del_command).rowcount
  print_to_stdout(f"{del_command} - rowcount={rowcount}")
  print_to_stdout(f"{del_command} - messages={cursor2.messages}")
  cursor2.commit()

      # set the newest records to the previous records.
  update_command = f"update Plex.accounting_period set ordinal=0 where pcn in ({pcn_list}) and ordinal = 1"
  rowcount=cursor2.execute(update_command).rowcount
  print_to_stdout(f"{update_command} - rowcount={rowcount}")
  print_to_stdout(f"{update_command} - messages={cursor2.messages}")
  cursor2.commit()


      # https://github.com/mkleehammer/pyodbc/wiki/Cursor
      # https://github.com/mkleehammer/pyodbc/wiki/Features-beyond-the-DB-API#fast_executemany
      # https://towardsdatascience.com/how-i-made-inserts-into-sql-server-100x-faster-with-pyodbc-5a0b5afdba5
      # insert records from Plex with ordinal = 1
  im2='''insert into Plex.accounting_period (pcn,period_key,period,period_display,fiscal_order,quarter_group,begin_date,end_date,period_status,add_date,update_date,ordinal) 
          values (?,?,?,?,?,?,?,?,?,?,?,1)''' 
      # im2='''insert into Scratch.accounting_period (pcn,period_key,period,period_display,fiscal_order,quarter_group,begin_date,end_date,period_status,add_date,update_date) 
      #         values (?,?,?,?,?,?,?,?,?,?,?)''' 

          #    2022-05-10 00:07:21.000
  cursor2.fast_executemany = True
  cursor2.executemany(im2,rows)
      # https://towardsdatascience.com/how-i-made-inserts-into-sql-server-100x-faster-with-pyodbc-5a0b5afdba5
  cursor2.commit()
  cursor2.close()

except pyodbc.Error as ex:
  ret = 1
  error_msg = ex.args[1]
  print_to_stderr(f"error {error_msg}") 
  print_to_stderr(f"error {ex.args}") 

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
    conn2.close()
  sys.exit(ret)
