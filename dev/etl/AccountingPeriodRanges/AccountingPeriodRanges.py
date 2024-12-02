#!/usr/bin/env python

#!/miniconda/bin/python
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
    pcn_list = (sys.argv[1])
    username = (sys.argv[2])
    password = (sys.argv[3])
    username2 = (sys.argv[4])
    password2 = (sys.argv[5])
    username3 = (sys.argv[6])
    password3 = (sys.argv[7])
    mysql_host = (sys.argv[8])
    mysql_port = (sys.argv[9])
    azure_dw = (sys.argv[10])

    # pcn_list = '123681,300758'
    # username = 'mg.odbcalbion'
    # password = 'Mob3xalbion'
    # username2 = 'mgadmin'
    # password2 = 'WeDontSharePasswords1!'
    # username3 = 'root'
    # password3 = 'password'    
    # mysql_host = 'reports03'
    # # mysql_host = 'reports13'
    # mysql_port = '31008'
    # azure_dw = '0'

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
    
    # accounting_period_ranges_dw_import
    # period range is min open period to year before it
    rowcount=cursor.execute("{call sproc123681_11728751_2112421 (?)}", pcn_list)
    rows = cursor.fetchall()
    print_to_stdout(f"call sproc123681_11728751_2112421 - rowcount={rowcount}")
    print_to_stdout(f"call sproc123681_11728751_2112421 - messages={cursor.messages}")

    cursor.close()
    fetch_time = datetime.now()
    tdelta = fetch_time - start_time 
    print_to_stdout(f"fetch_time={tdelta}") 

    if '1'==azure_dw:
        conn2 = pyodbc.connect('DSN=dw;UID='+username2+';PWD='+ password2 + ';DATABASE=mgdw')
        cursor2 = conn2.cursor()
        # https://code.google.com/archive/p/pyodbc/wikis/GettingStarted.wiki
        del_command = f"delete from Plex.accounting_period_ranges where pcn in ({pcn_list})"
        # del_command = f"delete from Scratch.accounting_balance_update_period_range where pcn in ({params})"
        # https://github.com/mkleehammer/pyodbc/wiki/Cursor
        # The return value is always the cursor itself:
        rowcount=cursor2.execute(del_command).rowcount
        print_to_stdout(f"{del_command} - rowcount={rowcount}")
        print_to_stdout(f"{del_command} - messages={cursor2.messages}")

        cursor2.commit()

        # https://github.com/mkleehammer/pyodbc/wiki/Cursor
        # https://github.com/mkleehammer/pyodbc/wiki/Features-beyond-the-DB-API#fast_executemany
        # https://towardsdatascience.com/how-i-made-inserts-into-sql-server-100x-faster-with-pyodbc-5a0b5afdba5
        im2='''insert into Plex.accounting_period_ranges (pcn,start_period,end_period,start_open_period,end_open_period,no_update)  
                values (?,?,?,?,?,0)''' 
        cursor2.fast_executemany = True
        cursor2.executemany(im2,rows)
        # https://towardsdatascience.com/how-i-made-inserts-into-sql-server-100x-faster-with-pyodbc-5a0b5afdba5
        cursor2.commit()
        cursor2.close()
 
    insertObject = []
    # columnNames = [column[0] for column in cursor.description]
    for record in rows:
        insertObject.append(tuple(record))

    conn3 = mysql.connector.connect(user=username3, password=password3,
                            host=mysql_host,
                            port=mysql_port,
                            database='Plex')
    cursor3 = conn3.cursor()
    # https://code.google.com/archive/p/pyodbc/wikis/GettingStarted.wiki
    del_command = f"delete from Plex.accounting_period_ranges where pcn in ({pcn_list})"
    cursor3.execute(del_command)
    # rowcount=cursor2.execute(txt.format(dellist = params)).rowcount
    print_to_stdout(f"{del_command} - rowcount={cursor3.rowcount}")
    # print_to_stdout(f"{txt} - messages={cursor2.messages}")
    conn3.commit()
    im2='''insert into Plex.accounting_period_ranges (pcn,start_period,end_period,start_open_period,end_open_period,no_update)  
            values (%s,%s,%s,%s,%s,0)''' 
    cursor3.executemany(im2,insertObject)
    # cursor2.executemany(im2,records_to_insert)
    conn3.commit()
    cursor3.close()

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
    if 'conn3' in globals():
        if conn3.is_connected():
            conn3.close()
    sys.exit(ret)
