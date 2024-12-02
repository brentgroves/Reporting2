#!/miniconda/bin/python

#!/miniconda/bin/python
#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python
#!/miniconda/bin/python # for docker image
#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python # for debugging
# https://www.webtrainingroom.com/python/excel-to-mysql-using-python
# https://linchpiner.github.io/k8s-multi-container-pods.html#:~:text=Why%20does%20Kubernetes%20allow%20more,efficiently%20communicate%2C%20ensuring%20data%20locality.
# https://gist.github.com/madan712/b01e85eeddecf9b92b53f8d3e11986d7
# https://www.webtrainingroom.com/python/excel-to-mysql-using-python
import pyodbc 
from datetime import datetime
import sys 
import mysql.connector
from mysql.connector import Error
import os
import xlsxwriter

# https://www.webtrainingroom.com/python/excel-to-mysql-using-python
# https://gist.github.com/madan712/b01e85eeddecf9b92b53f8d3e11986d7
# https://pythonbasics.org/write-excel/

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

# def fetch_table_data(table_name):
#     # The connect() constructor creates a connection to the MySQL server and returns a MySQLConnection object.
#     cnx = mysql.connector.connect(
#         host='localhost',
#         database='schema',
#         user='user',
#         password='password'
#     )

#     cursor = cnx.cursor()
#     cursor.execute('select * from ' + table_name)

#     header = [row[0] for row in cursor.description]

#     rows = cursor.fetchall()

#     # Closing connection
#     cnx.close()

#     return header, rows

try:
    ret = 0
    # pcn = (sys.argv[1])
    # username3 = (sys.argv[2])
    # password3 = (sys.argv[3])
    # mysql_host = (sys.argv[4])
    # mysql_port = (sys.argv[5])
    # start_period = (sys.argv[6])
    # end_period = (sys.argv[7])

    # pcn = '300758'
    pcn = '123681'
    username3 = 'root'
    password3 = 'password'   
    mysql_host = 'reports03'
    # mysql_host = 'reports13'
    mysql_port = '31008'
    start_period = 202209
    end_period = 202209

    # https://geekflare.com/calculate-time-difference-in-python/
    start_time = datetime.now()
    end_time = datetime.now()

    current_time = start_time.strftime("%m-%d-%Y_%H-%M-%S")
    print_to_stdout(f"Current Time: {current_time=}")

    table_name = f"TrialBalance-{current_time}"


    conn3 = mysql.connector.connect(user=username3, password=password3,
                            host=mysql_host,
                            port=mysql_port,
                            database='Report')

    cursor3 = conn3.cursor()
    # The parameters are needed in the call but the output params are not changed but are in result_args.
    result_args =cursor3.callproc('trial_balance', [start_period,end_period])
    #  https://www.mysqltutorial.org/calling-mysql-stored-procedures-python/
    # https://www.geeksforgeeks.org/what-does-the-double-star-operator-mean-in-python/
    # HOW TO EXAMINE MYSQL RESULT SET?
        # accounting_balance_append_period_range_dw_import
    # rowcount=cursor.execute("{call sproc300758_11728751_2000117 (?,?,?)}", pcn,start_period,end_period).rowcount
    # rows = cursor.fetchall()
    print_to_stdout(f"call trial_balance - rowcount={cursor3.rowcount}")

    # print out the result
    for result in cursor3.stored_results():
        # print(result.fetchall())
        rows = result.fetchall()

    header = ['period','category_type','category_name','sub_category_name','account_no','account_name','current_debit_credit','ytd_debit_credit']

    # Production
    # os.chdir('/app/output')
    # Development
    os.chdir('output')

    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(table_name + '.xlsx')
    worksheet = workbook.add_worksheet('MENU')

    # Create style for cells
    header_cell_format = workbook.add_format({'bold': True, 'border': True, 'bg_color': 'yellow'})
    body_cell_format = workbook.add_format({'border': True})

    row_index = 0
    column_index = 0

    for column_name in header:
        worksheet.write(row_index, column_index, column_name, header_cell_format)
        column_index += 1

    row_index = 1
    for row in rows:
        column_index = 0
        for column in row:
            worksheet.write(row_index, column_index, column, body_cell_format)
            # print(row_index, column_index, column)
            column_index += 1
        row_index += 1

    print_to_stdout(str(row_index) + ' rows written successfully to ' + workbook.filename)

    # Closing workbook
    workbook.close()


    fetch_time = datetime.now()
    tdelta = fetch_time - start_time 
    print_to_stdout(f"fetch_time={tdelta}") 

    # cursor3.commit()
    cursor3.close()

    # https://towardsdatascience.com/how-i-made-inserts-into-sql-server-100x-faster-with-pyodbc-5a0b5afdba5
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
    if 'conn3' in globals():
        if conn3.is_connected():
            conn3.close()
    sys.exit(ret)
