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
import pymongo
import os
from decimal import Decimal
from bson.decimal128 import Decimal128

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

# https://stackoverflow.com/questions/61456784/pymongo-cannot-encode-object-of-type-decimal-decimal
def convert_decimal(dict_item):
    # This function iterates a dictionary looking for types of Decimal and converts them to Decimal128
    # Embedded dictionaries and lists are called recursively.
    if dict_item is None: return None

    for k, v in list(dict_item.items()):
        if isinstance(v, dict):
            convert_decimal(v)
        elif isinstance(v, list):
            for l in v:
                convert_decimal(l)
        elif isinstance(v, Decimal):
            dict_item[k] = Decimal128(str(v))

    return dict_item

try:
  ret = 0
%PROD%pcn = (sys.argv[1])
%PROD%username11 = (sys.argv[4])
%PROD%password11 = (sys.argv[5])
%PROD%mongo_host = (sys.argv[9])
%PROD%mongo_port = (sys.argv[10])
%PROD%mongo_db = (sys.argv[11])

%DEV%pcn = '123681'
    # username2 = 'mgadmin'
    # password2 = 'WeDontSharePasswords1!'
%DEV%username11 = 'adminuser'
%DEV%password11 = "password123"
%DEV%mongo_host = '%MONGO_HOST%'
%DEV%mongo_port = '%MONGO_PORT%'
%DEV%mongo_db = '%MONGO_DB%'



  # https://geekflare.com/calculate-time-difference-in-python/
  start_time = datetime.now()
  end_time = datetime.now()

  current_time = start_time.strftime("%H:%M:%S")
  print_to_stdout(f"Current Time: {current_time}")

  conn3 = mysql.connector.connect(user=username3, password=password3,
                      host=mysql_host,
                      port=mysql_port,
                      database='Plex')

  cursor3 = conn3.cursor(dictionary=True)
  sql="select * from Plex.account_period_balance;"
  # sql="select * from Plex.account_period_balance limit 10;"
  cursor3.execute(sql)
  result3 = cursor3.fetchall()
  print(len(result3))

  account_period_balance=[]

  for x in result3:
    account_period_balance.append(convert_decimal(x))
  print(len(account_period_balance))
  # https://hevodata.com/learn/mysql-to-mongodb/    

  conn11 = f"mongodb://{mongo_host}:{mongo_port}/"  
  # mongo_host = "mongodb://localhost:27017/"
  # mongo_db = "mymongodb"
  client11 = pymongo.MongoClient(conn11)
  db11 = client11[mongo_db]


  col11 = db11["account_period_balance"]
  col11.delete_many({})
  if len(result3) > 0:
        x = col11.insert_many(account_period_balance) #myresult comes from mysql cursor
        print(len(x.inserted_ids))
        # use reports
        # db.account_period_balance.find( {} )
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
