# https://www.sqlshack.com/connect-azure-sql-database-using-python-from-ubuntu/
# https://learn.microsoft.com/en-us/sql/connect/python/python-driver-for-sql-server?view=sql-server-ver16
# https://docs.python-zeep.org/en/master/
# conda install -c anaconda pymssql

#import xmltodict
from zeep import Client
from zeep.transports import Transport

from requests import Session
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
import pyodbc
import os
import sys 
from datetime import datetime
import mysql.connector
from mysql.connector import Error



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
    # https://geekflare.com/calculate-time-difference-in-python/
    start_time = datetime.now()
    end_time = datetime.now()

    current_time = start_time.strftime("%H:%M:%S")
    print_to_stdout(f"Current Time: {current_time=}")

    # username = 'sa' 
    # password = 'buschecnc1' 
    # conn = pyodbc.connect('DSN=cm;UID='+username+';PWD='+ password + ';DATABASE=cribmaster')
    username2 = 'mgadmin'
    password2 = 'WeDontSharePasswords1!'

    conn2 = pyodbc.connect('DSN=dw;UID='+username2+';PWD='+ password2 + ';DATABASE=mgdw')
    cursor2 = conn2.cursor()

    select_statement =f'''select top 10 
    pcn,account_no,period,period_display
    ,debit,ytd_debit,credit,ytd_credit
    ,balance,ytd_balance
    from Plex.account_period_balance'''
    # print(select_statement)

    cursor2.execute(select_statement)
    rows = cursor2.fetchall()
    cursor2.close()

    print_to_stdout(f"{select_statement} - rowcount={len(rows)}")



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
    if 'conn2' in globals():
        conn2.close()
    sys.exit(ret)