#!/miniconda/bin/python

#!/miniconda/bin/python
#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python
#!/miniconda/bin/python # for docker image
#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python # for debugging
# https://docs.python-zeep.org/en/master/
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
    params = '123681,300758'
    username = 'MGAlbionReportsws@plex.com'
    password = '697fd42-084c-'
    username2 = 'mgadmin'
    password2 = 'WeDontSharePasswords1!'
    # params = (sys.argv[1])
    # username = (sys.argv[2])
    # password = (sys.argv[3])
    # username2 = (sys.argv[4])
    # password2 = (sys.argv[5])
    # print(f"params={params}")
    # print(f"params={params},username={username},password={password},username2={username2},password2={password2}")
    # sys.exit(0)
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
    
    rowcount=cursor.execute("{call sproc300758_11728751_1999565 (?)}", params)
    rows = cursor.fetchall()
    #  accounting_balance_update_period_range_dw_import
    print_to_stdout(f"call sproc300758_11728751_1999565 - rowcount={rowcount}")
    print_to_stdout(f"call sproc300758_11728751_1999565 - messages={cursor.messages}")

    cursor.close()
    fetch_time = datetime.now()
    tdelta = fetch_time - start_time 
    print_to_stdout(f"fetch_time={tdelta}") 

    conn2 = pyodbc.connect('DSN=dw;UID='+username2+';PWD='+ password2 + ';DATABASE=mgdw')

    cursor2 = conn2.cursor()
    # https://code.google.com/archive/p/pyodbc/wikis/GettingStarted.wiki
    del_command = f"delete from Plex.accounting_balance_update_period_range where pcn in ({params})"
    # del_command = f"delete from Scratch.accounting_balance_update_period_range where pcn in ({params})"

    # https://github.com/mkleehammer/pyodbc/wiki/Cursor
    # The return value is always the cursor itself:
    rowcount=cursor2.execute(del_command).rowcount
    print_to_stdout(f"{del_command} - rowcount={rowcount}")
    print_to_stdout(f"{del_command} - messages={cursor2.messages}")
    # https://github.com/mkleehammer/pyodbc/wiki/Cursor
    # https://github.com/mkleehammer/pyodbc/wiki/Features-beyond-the-DB-API#fast_executemany
    # https://towardsdatascience.com/how-i-made-inserts-into-sql-server-100x-faster-with-pyodbc-5a0b5afdba5
    im2='''insert into Plex.accounting_balance_update_period_range (pcn,period_start,period_end)  
            values (?,?,?)''' 
    # im2='''insert into Scratch.accounting_balance_update_period_range (pcn,period_start,period_end)  
    #         values (?,?,?)''' 

    cursor2.fast_executemany = True
    cursor2.executemany(im2,rows)

    # https://towardsdatascience.com/how-i-made-inserts-into-sql-server-100x-faster-with-pyodbc-5a0b5afdba5
except pyodbc.Error as ex:
    ret = 1
    error_msg = ex.args[1]
    print_to_stderr(f"error {error_msg}") 
    print_to_stderr(f"error {ex.args}") 

except BaseException as error:
    print('An exception occurred: {}'.format(error))

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
    sys.exit(ret)
