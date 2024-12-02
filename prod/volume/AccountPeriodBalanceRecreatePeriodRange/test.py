import pyodbc 
from datetime import datetime
import sys 
# https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver16
# https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/programming-guidelines?view=sql-server-ver16
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
    ret = 0
    start_time = datetime.now()
    end_time = datetime.now()
    params = (sys.argv[1])
    print(f"params={params}")
    sys.exit(0)
    # https://geekflare.com/calculate-time-difference-in-python/

    current_time = start_time.strftime("%H:%M:%S")
    print_to_stdout(f"Current Time: {current_time=}")

    # https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-1-configure-development-environment-for-pyodbc-python-development?view=sql-server-ver15
    username = 'mg.odbcalbion' 
    # password = 'wrong' 
    password = 'Mob3xalbion' 
    conn = pyodbc.connect('DSN=Plex;UID='+username+';PWD='+ password)
    # https://stackoverflow.com/questions/11451101/retrieving-data-from-sql-using-pyodbc
    cursor = conn.cursor()
    cursor.execute("{call sproc300758_11728751_1978024 (?)}", params)
    rows = cursor.fetchall()
    cursor.close()
    fetch_time = datetime.now()
    tdelta = fetch_time - start_time 
    print_to_stdout(f"fetch_time={tdelta}") 

    username = 'mgadmin' 
    password = 'WeDontSharePasswords1!' 
    conn2 = pyodbc.connect('DSN=dw;UID='+username+';PWD='+ password + ';DATABASE=mgdw')

    cursor2 = conn2.cursor()
    # https://code.google.com/archive/p/pyodbc/wikis/GettingStarted.wiki
    txt = "delete from Scratch.accounting_account_06_03 where pcn in ({dellist:s})"
    # https://github.com/mkleehammer/pyodbc/wiki/Cursor
    # The return value is always the cursor itself:
    rowcount=cursor2.execute(txt.format(dellist = params)).rowcount
    print_to_stdout(f"{txt} - rowcount={rowcount}")
    print_to_stdout(f"{txt} - messages={cursor2.messages}")
    # https://github.com/mkleehammer/pyodbc/wiki/Cursor
    # https://github.com/mkleehammer/pyodbc/wiki/Features-beyond-the-DB-API#fast_executemany
    # https://towardsdatascience.com/how-i-made-inserts-into-sql-server-100x-faster-with-pyodbc-5a0b5afdba5
    im2='''insert into Scratch.accounting_account_06_03
    values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''' 
    # rec = [(123681,629753,'10000-000-00000','Cash - Comerica General',0,'Asset',0,'category-name-legacy','cattypeleg',0,'subcategory-name-legacy','subcattleg',0,201604)]
    cursor2.fast_executemany = True
    cursor2.executemany(im2,rows)
    print_to_stdout(f"{im2} - rowcount={rowcount}")
    print_to_stdout(f"{im2} - messages={cursor2.messages}")
    # https://towardsdatascience.com/how-i-made-inserts-into-sql-server-100x-faster-with-pyodbc-5a0b5afdba5

except pyodbc.Error as ex:
    ret = 1
    error_msg = ex.args[1]
    print_to_stderr(error_msg) 

finally:
    end_time = datetime.now()
    tdelta = end_time - start_time 
    print_to_stdout(f"total time: {tdelta}") 
    if 'conn' in globals():
        conn.close()
    if 'cursor2' in globals():
        cursor2.commit()
        cursor2.close()
    if 'conn2' in globals():
        conn2.close()
    # sys.exit(ret)
