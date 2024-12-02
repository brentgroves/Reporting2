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
    # # pcn_list = '123681,300758,310507,306766,300757'
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

    if '1'==azure_dw:
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

    insertObject = []
    # columnNames = [column[0] for column in cursor.description]
    for record in rows:
      insertObject.append(tuple(record))

    # conn2 = pyodbc.connect('DSN=dw;UID='+username2+';PWD='+ password2 + ';DATABASE=mgdw')

    conn3 = mysql.connector.connect(user=username3, password=password3,
                              host=mysql_host,
                              port=mysql_port,
                              database='Plex')
    # conn3 = mysql.connector.connect(user='root', password='password',
    #                           host='10.1.0.116',
    #                           port='31008',
    #                           database='mcpdw')

    cursor3 = conn3.cursor()
    # https://code.google.com/archive/p/pyodbc/wikis/GettingStarted.wiki
    # txt = "delete from Plex.accounting_account where pcn in ({dellist:s})"
    txt = "delete from Plex.accounting_account where pcn in ({dellist:s})"
    # https://github.com/mkleehammer/pyodbc/wiki/Cursor
    # The return value is always the cursor itself:
    cursor3.execute(txt.format(dellist = pcn_list))
    # rowcount=cursor2.execute(txt.format(dellist = params)).rowcount
    print_to_stdout(f"{txt} - rowcount={cursor3.rowcount}")
    # print_to_stdout(f"{txt} - messages={cursor2.messages}")

    conn3.commit()

    # https://github.com/mkleehammer/pyodbc/wiki/Cursor
    # https://github.com/mkleehammer/pyodbc/wiki/Features-beyond-the-DB-API#fast_executemany
    # https://towardsdatascience.com/how-i-made-inserts-into-sql-server-100x-faster-with-pyodbc-5a0b5afdba5
    # im2='''insert into test.accounting_account
    # values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''' 
    # mySql_insert_query = """INSERT INTO Laptop (Id, Name, Price, Purchase_date) 
    #                        VALUES (%s, %s, %s, %s) """
    im2 = """INSERT INTO Plex.accounting_account VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
    # im2 = """INSERT INTO test.accounting_account VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """

    # rec = [(123681,629753,'10000-000-00000','Cash - Comerica General',0,'Asset',0,'category-name-legacy','cattypeleg',0,'subcategory-name-legacy','subcattleg',0,201604)]
    # cursor2.fast_executemany = True

    # records_to_insert = [(123681,629753,'10000-000-00000','Cash - Comerica General',0,'Asset',0,'category-name-legacy','cattypeleg',0,'subcategory-name-legacy','subcattleg',0,201604),
    #                     (123681,629754,'10000-000-00000','Cash - Comerica General',0,'Asset',0,'category-name-legacy','cattypeleg',0,'subcategory-name-legacy','subcattleg',0,201604),
    #                     (123681,629755,'10000-000-00000','Cash - Comerica General',0,'Asset',0,'category-name-legacy','cattypeleg',0,'subcategory-name-legacy','subcattleg',0,201604)]

    cursor3.executemany(im2,insertObject)
    # cursor2.executemany(im2,records_to_insert)
    conn3.commit()
    cursor3.close()

    # cursor2.executemany(im2,insertObject)
    # https://towardsdatascience.com/how-i-made-inserts-into-sql-server-100x-faster-with-pyodbc-5a0b5afdba5
# Error while connecting to MySQL Failed executing the operation; Could not process parameters: 
# Row((123681, 629753, '10000-000-00000', 'Cash - Comerica General', 0, 'Asset', 0, '', '', 0, '', '', 0, 201604)), 
# it must be of type list, tuple or dict
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
    if 'conn3' in globals():
        if conn3.is_connected():
            conn3.close()
            # print("MySQL connection is closed")
    sys.exit(ret)
