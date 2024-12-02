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

    # pcn = '123681'
    # username2 = 'mgadmin'
    # password2 = 'WeDontSharePasswords1!'
    # username3 = 'root'
    # password3 = 'password'   
    # mysql_host = 'reports03'
    # mysql_port = '31008'
    # azure_dw = '0'

    # https://geekflare.com/calculate-time-difference-in-python/
    start_time = datetime.now()
    end_time = datetime.now()

    current_time = start_time.strftime("%H:%M:%S")
    print_to_stdout(f"Current Time: {current_time}")

    conn3 = mysql.connector.connect(user=username3, password=password3,
                        host=mysql_host,
                        port=mysql_port,
                        database='Plex')

    mycursor = mysqldb.cursor(dictionary=True)
    sql="select * from Plex.account_period_balance limit 10;"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    
    print(myresult)
        # cursor3.callproc('account_period_balance_recreate_period_range', [pcn])
        # # rowcount=cursor2.execute(txt.format(dellist = params)).rowcount
        # print_to_stdout(f"call Plex.account_period_balance_recreate_period_range() - rowcount={cursor3.rowcount}")
        # # print_to_stdout(f"{txt} - messages={cursor2.messages}")
    # conn3.commit()
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
