#!/usr/bin/env python
# https://evanhahn.com/python-skip-header-csv-reader/
# https://realpython.com/python-csv/
import pyodbc 
import csv, sys
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
# %DEV%pcn = '123681'
# # pcn = '300758'
  username2 = 'mgadmin' 
  password2 = 'WeDontSharePasswords1!' 
  username3 = 'root'
  password3 = 'password'
# %DEV%username4 = 'MGEdonReportsws@plex.com'
# %DEV%password4 = '9f45e3d-67ed-'
  mysql_host = 'reports31'
# # mysql_host = 'reports13'
  mysql_port = '30031'
  azure_dw = '1'
  start_period = 202305
  end_period = 202305

# %PROD%pcn = (sys.argv[1])
# %PROD%username = (sys.argv[2])
# %PROD%password = (sys.argv[3])
# %PROD%username2 = (sys.argv[4])
# %PROD%password2 = (sys.argv[5])
# %PROD%username3 = (sys.argv[6])
# %PROD%password3 = (sys.argv[7])
# %PROD%mysql_host = (sys.argv[8])
# %PROD%mysql_port = (sys.argv[9])
# %PROD%azure_dw = (sys.argv[10])

# %DEV%pcn_list = '123681,300758'
#     # # pcn_list = '123681,300758,310507,306766,300757'
# %DEV%username = 'mg.odbcalbion'
# %DEV%password = 'Mob3xalbion'
# %DEV%username2 = 'mgadmin'
# %DEV%password2 = 'WeDontSharePasswords1!'
# %DEV%username3 = 'root'
# %DEV%password3 = 'password'
# %DEV%mysql_host = '%MYSQL_HOST%'
#     # # mysql_host = 'reports13'
# %DEV%mysql_port = '%MYSQL_PORT%'
# %DEV%azure_dw = '%AZURE_DW%'

  filename = 'Trial_Balance.csv'
  # with open(filename, newline='') as f:
  with open(filename, "r") as csvfile:
    csvreader = csv.reader(csvfile)
    # This skips the first row of the CSV file.
    next(csvreader)
    rows=[]
    pcn=123681
    for row in csvreader:
        if "Total" != row[0]:
            # print(row)
            period_display= row[0]
            period=period_display[-4:]+period_display[:2]
            category_type=row[1]
            category_name=row[2]
            sub_category_name=row[3]
            account_no=row[4]
            account_name=row[5]
            # string[start:end:step]
            # set period = cast (right(period_display,4) + left(period_display,2) as int), -- Southfield
            # period=''
            current_debit_credit=str(round(float(row[6]),2))
            # ytd_debit_credit=row[7]
            ytd_debit_credit=str(round(float(row[7]),2))
            rows.append((pcn,period,period_display,category_type,category_name,sub_category_name,account_no,account_name,current_debit_credit,ytd_debit_credit))
            # rows.append((pcn,period,period_display,ytd_debit_credit))
        # print(row)
  if '1'==azure_dw:
    conn2 = pyodbc.connect('DSN=dw;UID='+username2+';PWD='+ password2 + ';DATABASE=mgdw')
    cursor2 = conn2.cursor()
    # https://stackoverflow.com/questions/32748982/does-pyodbc-support-any-form-of-named-parameters
    cursor2.execute("delete from Plex.trial_balance_multi_level_py where period between ? and ?", (start_period, end_period))
    cursor2.commit()
    # im2='''insert into Plex.trial_balance_multi_level_py(pcn,period,period_display,ytd_debit_credit)
    # values (?,?,?,?)''' 
    im2='''insert into Plex.trial_balance_multi_level_py(pcn,period,period_display,category_type,category_name,sub_category_name,account_no,account_name,current_debit_credit,ytd_debit_credit)
    values (?,?,?,?,?,?,?,?,?,?)''' 
    # rec = [(123681,629753,'10000-000-00000','Cash - Comerica General',0,'Asset',0,'category-name-legacy','cattypeleg',0,'subcategory-name-legacy','subcattleg',0,201604)]
    cursor2.fast_executemany = True
    cursor2.executemany(im2,rows)
    cursor2.commit()

  conn3 = mysql.connector.connect(user=username3, password=password3,
                            host=mysql_host,
                            port=mysql_port,
                            database='Plex')

  cursor3 = conn3.cursor()
  # https://stackoverflow.com/questions/7929364/python-best-practice-and-securest-way-to-connect-to-mysql-and-execute-queries/7929842#7929842
  # cursor.execute("SELECT spam FROM eggs WHERE lumberjack = ?", (lumberjack,))
  cursor3.execute("delete from Plex.trial_balance_multi_level_py where period between %s and %s", (start_period, end_period))
  conn3.commit()

  # https://towardsdatascience.com/how-i-made-inserts-into-sql-server-100x-faster-with-pyodbc-5a0b5afdba5
  im2 ='''insert into Plex.trial_balance_multi_level_py (pcn,period,period_display,category_type,category_name,sub_category_name,account_no,account_name,current_debit_credit,ytd_debit_credit)
              VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '''

# insert into Plex.trial_balance_multi_level
# values
# (123681,'112-1111')
  cursor3.executemany(im2,rows)
  # cursor2.executemany(im2,records_to_insert)
  conn3.commit()
except csv.Error as e:
    ret = 1
    print_to_stderr("csv Error", e)
    # sys.exit('file {}, line {}: {}'.format(filename, csvreader.line_num, e))

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
    # end_time = datetime.now()
    # tdelta = end_time - start_time 
    # print_to_stdout(f"total time: {tdelta}") 
    # if 'conn' in globals():
    #     conn.close()
    if 'conn2' in globals():
        conn2.close()
    if 'conn3' in globals():
        if conn3.is_connected():
            conn3.close()
            # print("MySQL connection is closed")
    sys.exit(ret)
# https://evanhahn.com/python-skip-header-csv-reader/
# with open("mycsv.csv", "r") as csvfile:
#     csvreader = csv.DictReader(csvfile)
#     for row in csvreader:
#         print(row["Date"], row["Description"], row["Amount"])        
# ['Period', 'Category Type', 'Category Name', 'Sub Category Name', 'No', 'Name', 'Current Debit/(Credit)', 'YTD Debit/(Credit)']
# pcn=123681
# account_no=row[4]
# account_name=row[5]
# category_type=row[1]
# period=nothing
# set period = cast (right(period_display,4) + left(period_display,2) as int), -- Southfield
# period_display= row[0]
# category_name=row[2]
# sub_category_name=row[3]
# current_debit_credit=row[6]
# ytd_debit_credit=row[7]

