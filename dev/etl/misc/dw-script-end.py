#!/usr/bin/env python

#!/miniconda/bin/python 
# https://docs.python-zeep.org/en/master/

import pyodbc 
from datetime import datetime
import sys 
import mysql.connector
from mysql.connector import Error

# https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver16
# https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/programming-guidelines?view=sql-server-ver16
# remember to source oaodbc64.sh to set env variables.
# remember to source oaodbc64.sh to set env variables.
# remember to source oaodbc64.sh to set env variables.
# https://github.com/mkleehammer/pyodbc/wiki/Calling-Stored-Procedures
# https://thepythonguru.com/fetching-records-using-fetchone-and-fetchmany/
# https://code.google.com/archive/p/pyodbc/wikis/Cursor.wiki
def print_to_stdout(*a):
    # Here a is the array holding the objects
    # passed as the argument of the function
    print(*a, file = sys.stdout)

def print_to_stderr(*a):
    # Here a is the array holding the objects
    # passed as the argument of the function
    print(*a, file = sys.stderr)
    # InterfaceError('IM002', '[IM002] [unixODBC][Driver Manager]Data source name not found and no default driver specified (0) (SQLDriverConnect)')
try:
    script_key = (sys.argv[1])
    error_bit = int((sys.argv[2])) # need an integer for mysql call
    username3 = (sys.argv[3])
    password3 = (sys.argv[4])
    mysql_host = (sys.argv[5])
    mysql_port = (sys.argv[6])

    # script_key = '4'
    # error_bit = int('0')
    # username3 = 'root'
    # password3 = 'password'    # print(f"params={params}")
    # mysql_host = 'reports13'
    # mysql_port = '31008'

    ret = 0
    # https://geekflare.com/calculate-time-difference-in-python/
    start_time = datetime.now()
    end_time = datetime.now()

    current_time = start_time.strftime("%H:%M:%S")
    print_to_stdout(f"Current Time: {current_time=}")


    conn3 = mysql.connector.connect(user=username3, password=password3,
                            host=mysql_host,
                            port=mysql_port,
                            database='ETL')

    cursor3 = conn3.cursor()
    # cursor2.callproc('get_laptop', [1, ])
    cursor3.callproc('script_end', [script_key,error_bit])
    # https://mysqlcode.com/call-mysql-stored-procedure-in-python/
    # cursor2.callproc('ETL.script_start', ["1"])
    # cursor2.execute("{call ETL.script_start (?)}", script_key)
    conn3.commit()
    cursor3.close()


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
    if 'conn3' in globals():
        if conn3.is_connected():
            conn3.close()
    sys.exit(ret)
