#!/usr/bin/env python

#!/miniconda/bin/python # for docker image
#!/miniconda/bin/python
#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python # for debugging
#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python
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

%DEV%pcn_list = '123681,300758'
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
  print_to_stdout(f"Current Time: {current_time=}")

  # https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-1-configure-development-environment-for-pyodbc-python-development?view=sql-server-ver15
  # password = 'wrong' 
  conn = pyodbc.connect('DSN=Plex;UID='+username+';PWD='+ password)
  # https://stackoverflow.com/questions/11451101/retrieving-data-from-sql-using-pyodbc
  cursor = conn.cursor()
# accounting_account_DW_Import
  cursor.execute("{call sproc300758_11728751_1978024 (?)}", pcn_list)
  rows = cursor.fetchall()
  # insertObject.append(rows[0])
  # insertObject.append((123681,629753,'10000-000-00000','Cash - Comerica General',0,'Asset',0,'category-name-legacy','cattypeleg',0,'subcategory-name-legacy','subcattleg',0,201604))
  # for record in rows:
  #     insertObject.append( record  )
      # insertObject.append( dict( zip( columnNames , record ) ) )

    

# Error while connecting to MySQL Failed executing the operation; Could not process parameters: 
# Row((123681, 629753, '10000-000-00000', 'Cash - Comerica General', 0, 'Asset', 0, '', '', 0, '', '', 0, 201604)), 
# it must be of type list, tuple or dict

  cursor.close()
  fetch_time = datetime.now()
  tdelta = fetch_time - start_time 
  print_to_stdout(f"fetch_time={tdelta}") 
  # https://dev.mysql.com/doc/connector-python/en/connector-python-introduction.html
  # elf-contained driver. Connector/Python does not require the MySQL client library or any Python modules outside the standard library.
  # https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html
  conn2 = pyodbc.connect('DSN=dw;UID='+username2+';PWD='+ password2 + ';DATABASE=mgdw')
  cursor2 = conn2.cursor()
      # https://code.google.com/archive/p/pyodbc/wikis/GettingStarted.wiki
      # txt = "delete from Plex.accounting_account where pcn in ({dellist:s})"
  txt = "delete from Plex.accounting_account where pcn in ({dellist:s})"
  # https://github.com/mkleehammer/pyodbc/wiki/Cursor
  # The return value is always the cursor itself:
  rowcount=cursor2.execute(txt.format(dellist = pcn_list)).rowcount
  print_to_stdout(f"{txt} - rowcount={rowcount}")
  print_to_stdout(f"{txt} - messages={cursor2.messages}")
      
  cursor2.commit()
  # https://github.com/mkleehammer/pyodbc/wiki/Cursor
  # https://github.com/mkleehammer/pyodbc/wiki/Features-beyond-the-DB-API#fast_executemany
  # https://towardsdatascience.com/how-i-made-inserts-into-sql-server-100x-faster-with-pyodbc-5a0b5afdba5
  # im2='''insert into Plex.accounting_account
  # values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''' 
  im2='''insert into Plex.accounting_account
  values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''' 
  # rec = [(123681,629753,'10000-000-00000','Cash - Comerica General',0,'Asset',0,'category-name-legacy','cattypeleg',0,'subcategory-name-legacy','subcattleg',0,201604)]
  cursor2.fast_executemany = True
  cursor2.executemany(im2,rows)
  cursor2.commit()
  cursor2.close()

except pyodbc.Error as ex:
  ret = 1
  error_msg = ex.args[1]
  print_to_stderr(error_msg) 

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
    if 'conn' in globals():
        conn.close()
    if 'conn2' in globals():
        conn2.close()
    sys.exit(ret)
