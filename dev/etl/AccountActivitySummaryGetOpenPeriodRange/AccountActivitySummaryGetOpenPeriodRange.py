#!/usr/bin/env python

#!/miniconda/bin/python
#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python
#!/miniconda/bin/python # for docker image
#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python # for debugging

# https://docs.python-zeep.org/en/master/
#import xmltodict
from zeep import Client
from requests import Session
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from zeep import Client
from zeep.transports import Transport
import pyodbc
from datetime import datetime
import sys 
import os
import mysql.connector
from mysql.connector import Error

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
  # pcn = (sys.argv[1])
  # username2 = (sys.argv[2])
  # password2 = (sys.argv[3])
  # username3 = (sys.argv[4])
  # password3 = (sys.argv[5])
  # username4 = (sys.argv[6])
  # password4 = (sys.argv[7])
  # mysql_host = (sys.argv[8])
  # mysql_port = (sys.argv[9])
  # azure_dw = (sys.argv[10])

  pcn = '123681'
  # pcn = '300758'
  username2 = 'mgadmin' 
  password2 = 'WeDontSharePasswords1!' 
  username3 = 'root'
  password3 = 'password'
  username4 = 'MGEdonReportsws@plex.com'
  password4 = '9f45e3d-67ed-'
  mysql_host = 'reports03'
  # mysql_host = 'reports13'
  mysql_port = '31008'
  azure_dw = '0'


  # https://geekflare.com/calculate-time-difference-in-python/
  start_time = datetime.now()
  end_time = datetime.now()

  current_time = start_time.strftime("%H:%M:%S")
  print_to_stdout(f"Current Time: {current_time}")

  conn3 = mysql.connector.connect(user=username3, password=password3,
                          host=mysql_host,
                          port=mysql_port,
                          database='Plex')

  cursor3 = conn3.cursor()
  start_period = 0
  end_period = 0
  start_open_period = 0
  end_open_period = 0
  no_update = 9
  # The parameters are needed in the call but the output params are not changed but are in result_args.
  result_args =cursor3.callproc('accounting_get_period_ranges', [pcn,start_period,end_period,start_open_period,end_open_period,no_update])
  # result_args =cursor3.callproc('accounting_balance_get_period_range', [123681,period_start2,period_end2])
  #  https://www.mysqltutorial.org/calling-mysql-stored-procedures-python/
  # start_period = result_args[1] #param 2
  # end_period = result_args[2] #param 3
  start_open_period = result_args[3] #param 4
  end_open_period = result_args[4] #param 5
  # no_update = result_args[5] #param 6
  period = start_open_period

  year = period // 100
  # Get Max fiscal period
  max_fiscal_period = 0
  # The parameters are needed in the call but the output params are not changed but are in result_args.
  result_args =cursor3.callproc('max_fiscal_period', [pcn,year,max_fiscal_period])
  max_fiscal_period = result_args[2] #param 3


  # https://docs.python-zeep.org/en/master/transport.html?highlight=authentication#http-authentication
  session = Session()
  session.auth = HTTPBasicAuth(username4,password4)
  # session.auth = HTTPBasicAuth('MGEdonReportsws@plex.com','9f45e3d-67ed-')

  client = Client(wsdl='../wsdl/Plex_SOAP_prod.wsdl',transport=Transport(session=session)) # prod
  # client = Client(wsdl='dev/etl/wsdl/Plex_SOAP_prod.wsdl',transport=Transport(session=session)) # stand-alone .
  
  # https://docs.python-zeep.org/en/master/datastructures.html
  e_type = client.get_type('ns0:ExecuteDataSourceRequest')
  a_ip_type = client.get_type('ns0:ArrayOfInputParameter')
  ip_type=client.get_type('ns0:InputParameter')
  ip_pcn = ip_type(Value=pcn,Name='@PCNs',Required=False,Output=False)


  while period <= end_open_period:
    ip_period_start = ip_type(Value=period,Name='@Period_Start',Required=True,Output=False)
    ip_period_end = ip_type(Value=period,Name='@Period_End',Required=True,Output=False)
    Parameters=a_ip_type([ip_pcn,ip_period_start,ip_period_end])

    # e=e_type(DataSourceKey=8619,InputParameters=[{'Value':'4/26/2022','Name':'@Report_Date','Required':False,'Output':False}],DataSourceName='Detailed_Production_Get_New')
    e=e_type(DataSourceKey=4814,InputParameters=Parameters,DataSourceName='Account_Activity_Summary_xPCN_Get')

    response = client.service.ExecuteDataSource(e)
    # print(response['OutputParameters'])

  # Section for determining column indexes  
    # column_list = response['ResultSets'].ResultSet[0].Rows.Row[0].Columns.Column
    # column_names=""
    # column_values=""
    # dic ={}
    # ind=0
    # for j in column_list:
    #   dic.update({j.Name:ind}) 
    #   print(str(ind) + '-' + j.Name)
    #   ind=ind+1

    # print(dic)

    # collect desired columns of the result set into a list  
    list = response['ResultSets'].ResultSet[0].Rows.Row
    rec=[]
    row=0
    for i in list:
      # balance = float(i.Columns.Column[5].Value)-float(i.Columns.Column[6].Value)
      # str(round(float(i.Columns.Column[5].Value)-float(i.Columns.Column[6].Value),5)),

      rec.append((pcn,period,
      i.Columns.Column[1].Value,
      i.Columns.Column[4].Value,
      i.Columns.Column[5].Value,
      i.Columns.Column[6].Value,
      str(round(float(i.Columns.Column[5].Value)-float(i.Columns.Column[6].Value),5)),
      # i.Columns.Column[5].Value-i.Columns.Column[6].Value,
      i.Columns.Column[7].Value))
      # debug section
      # print(rec[row])
      # row=row+1

    if '1'==azure_dw:
      conn2 = pyodbc.connect('DSN=dw;UID='+username2+';PWD='+ password2 + ';DATABASE=mgdw',timeout=30)
      # conn2.timeout = 10
      # conn2.autocommit = True
      cursor2 = conn2.cursor()

      
      # https://code.google.com/archive/p/pyodbc/wikis/GettingStarted.wiki
      sql = "delete from Plex.account_activity_summary WHERE pcn = ? and period = ?"
      rowcount=cursor2.execute(sql, (pcn,period)).rowcount
      print_to_stdout(f"delete from Plex.account_activity_summary - rowcount={rowcount}")
      print_to_stdout(f"delete from Plex.account_activity_summary - messages={cursor2.messages}")
      cursor2.commit()

      im2 ='''insert into Plex.account_activity_summary (pcn,period,account_no,beginning_balance,debit,credit,balance,ending_balance)
      values (?,?,?,?,?,?,?,?)'''
      # test = rec[0:500]
      cursor2.fast_executemany = True
      cursor2.executemany(im2,rec) 
      cursor2.commit()

    cursor3.execute(f"delete from Plex.account_activity_summary WHERE pcn = {pcn} and period = {period}")
    # rowcount=cursor2.execute(txt.format(dellist = params)).rowcount
    print_to_stdout(f"delete from Plex.account_activity_summary - rowcount={cursor3.rowcount}")
    # print_to_stdout(f"{txt} - messages={cursor2.messages}")
    conn3.commit()

    # https://github.com/mkleehammer/pyodbc/wiki/Cursor
    # https://github.com/mkleehammer/pyodbc/wiki/Features-beyond-the-DB-API#fast_executemany
    # https://towardsdatascience.com/how-i-made-inserts-into-sql-server-100x-faster-with-pyodbc-5a0b5afdba5
    im2 ='''insert into Plex.account_activity_summary (pcn,period,account_no,beginning_balance,debit,credit,balance,ending_balance)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s) '''

    cursor3.executemany(im2,rec)
    # cursor2.executemany(im2,records_to_insert)
    conn3.commit()
  
    if (period < max_fiscal_period):
      period = period + 1
    else:
      period = (year+1)*100 + 1
    # print_to_stdout(f"period={period}")

  if '1'==azure_dw:
    cursor2.close()
  cursor3.close()

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
    if 'conn3' in globals():
        if conn3.is_connected():
            conn3.close()
            # print("MySQL connection is closed")
    sys.exit(ret)

# #python -mzeep Plex_SOAP_test.wsdl
# # https://www.youtube.com/watch?v=JBYEQjg_znI
# # request = '<ExecuteDataSourceRequest xmlns="http://www.plexus-online.com/DataSource"><DataSourceKey>8619</DataSourceKey><InputParameters><InputParameter><Value>4/26/2022</Value><Name>@Report_Date</Name><Required>false</Required><Output>false</Output></InputParameter></InputParameters><DataSourceName>Detailed_Production_Get_New</DataSourceName></ExecuteDataSourceRequest>'

# # request = '''<ExecuteDataSourceRequest xmlns="http://www.plexus-online.com/DataSource">
# #     <DataSourceKey>8619</DataSourceKey>
# #     <InputParameters>
# #       <InputParameter>
# #         <Value>4/26/2022</Value>
# #         <Name>@Report_Date</Name>
# #         <Required>false</Required>
# #         <Output>false</Output>
# #       </InputParameter>
# #     </InputParameters>
# #     <DataSourceName>Detailed_Production_Get_New</DataSourceName>
# #   </ExecuteDataSourceRequest>'''
# # print(request)
# # client.service.ExecuteDataSource(request)