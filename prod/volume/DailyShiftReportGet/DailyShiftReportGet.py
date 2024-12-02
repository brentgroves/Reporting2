#!/usr/bin/env python

#!/miniconda/bin/python
#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python
#!/miniconda/bin/python # for docker image

import string
import sys
from datetime import datetime, timedelta

import mysql.connector
import pyodbc
from mysql.connector import Error
from requests import Session
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
# https://docs.python-zeep.org/en/master/
#import xmltodict
from zeep import Client
from zeep.transports import Transport


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
  pcn = (sys.argv[1])
  username2 = (sys.argv[2])
  password2 = (sys.argv[3])
  username3 = (sys.argv[4])
  password3 = (sys.argv[5])
  wsusername = (sys.argv[6])
  wspassword = (sys.argv[7])

#   pcn = '123681'
  # pcn = '300758'
#   username2 = 'mgadmin' 
#   password2 = 'WeDontSharePasswords1!' 
#   username3 = 'root'
#   password3 = 'password'
  # username4 = 'MGEdonReportsws@plex.com'
  # password4 = '9f45e3d-67ed-'
#   username4 = 'MGAlbionReportsws@plex.com'
#   password4 = '697fd42-084c-'
  # username4 = 'MGAlabamaReportsws@plex.com'
  # password4 = '957f15d-813d-'
  # username4 = 'MGAvillaReportsws@plex.com@mobexglobal.com'
  # password4 = '56e1f6c-7323-'
  # username4 = 'MGEdonReportsws@plex.com'
  # password4 = '9f45e3d-67ed-'
  # username4 = 'MGAFPReportsws@plex.com'
  # password4 = 'c65a4d9-641f-'
  # https://geekflare.com/calculate-time-difference-in-python/
  start_time = datetime.now()
  end_time = datetime.now()

  current_time = start_time.strftime("%H:%M:%S")
  print_to_stdout(f"Current Time: {current_time=}")



  # https://docs.python-zeep.org/en/master/transport.html?highlight=authentication#http-authentication
  session = Session()
  session.auth = HTTPBasicAuth(wsusername,wspassword)
  # session.auth = HTTPBasicAuth('MGEdonReportsws@plex.com','9f45e3d-67ed-')
  # client = Client(wsdl='/home/bgroves@BUSCHE-CNC.COM/srcpy/python-train/etl/wsdl/Plex_SOAP_prod.wsdl',transport=Transport(session=session)) # ETL-pod
  client = Client(wsdl='../wsdl/Plex_SOAP_prod.wsdl',transport=Transport(session=session)) # ETL-pod
  # client = Client(wsdl='etl/wsdl/Plex_SOAP_prod.wsdl',transport=Transport(session=session)) # python-train

  # https://docs.python-zeep.org/en/master/datastructures.html
  e_type = client.get_type('ns0:ExecuteDataSourceRequest')
  a_ip_type = client.get_type('ns0:ArrayOfInputParameter')
  ip_type=client.get_type('ns0:InputParameter')

  # Get today's date
  today = datetime.today()
  # print("Today is: ", today)
  
  # Yesterday date
  yesterday = today - timedelta(days = 1)
  start_end_date=yesterday.strftime("%m/%d/%Y")
  # print("Yesterday was: ", yesterday.strftime("%m/%d/%Y"))
  ip_start_date = ip_type(Value=start_end_date,Name='@Start_Date',Required=True,Output=False)
  ip_end_date = ip_type(Value=start_end_date,Name='@End_Date',Required=False,Output=False)
  # ip_pcn = ip_type(Value=pcn,Name='@PCNs',Required=False,Output=False)
  Parameters=a_ip_type([ip_start_date,ip_end_date])

  # e=e_type(DataSourceKey=8619,InputParameters=[{'Value':'4/26/2022','Name':'@Report_Date','Required':False,'Output':False}],DataSourceName='Detailed_Production_Get_New')
  e=e_type(DataSourceKey=9726,InputParameters=Parameters,DataSourceName='Daily_Shift_Report_Get')

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
  # sys.exit(0)


  report_date=yesterday.strftime("%Y-%m-%d")+' 00:00:00'

  # collect desired columns of the result set into a list  
  list = response['ResultSets'].ResultSet[0].Rows.Row
  rec=[]
  row=0
  for i in list:
    # balance = float(i.Columns.Column[5].Value)-float(i.Columns.Column[6].Value)
    # str(round(float(i.Columns.Column[5].Value)-float(i.Columns.Column[6].Value),5)),
#     is_nice = True
# state = "nice" if is_nice else "not nice"
    # if i.Columns.Column[9].Value==None:
    #   print(f'none detected {i.Columns.Column[9].Value}')
    rec.append((pcn,report_date,
    i.Columns.Column[5].Value, # workcenter_key
    i.Columns.Column[6].Value, # workcenter_code
    i.Columns.Column[7].Value, # part_key
    i.Columns.Column[8].Value, # part_no 
    i.Columns.Column[9].Value if i.Columns.Column[9].Value is not None else '', # part_revision
    i.Columns.Column[10].Value, # part_name
    i.Columns.Column[11].Value, # operation_no
    i.Columns.Column[12].Value, # operation_code 
    i.Columns.Column[15].Value, # parts_produced
    i.Columns.Column[16].Value, # parts_scrapped
    round(float(i.Columns.Column[21].Value),2), # earned_hours 
    round(float(i.Columns.Column[22].Value),2), # actual_hours 
    #  str(round(float(i.Columns.Column[5].Value)-float(i.Columns.Column[6].Value),5)),
    i.Columns.Column[26].Value, # part_operation_key
    i.Columns.Column[27].Value, # quantity_produced
    i.Columns.Column[29].Value, # labor_rate
    ))
    # debug section
    # print(rec[row])
    # row=row+1


  conn2 = pyodbc.connect('DSN=dw;UID='+username2+';PWD='+ password2 + ';DATABASE=mgdw',timeout=30)
  # conn2.timeout = 10
  # conn2.autocommit = True
  cursor2 = conn2.cursor()

  # https://code.google.com/archive/p/pyodbc/wikis/GettingStarted.wiki
  sql ='''
  delete from DailyMetrics.daily_shift_report
  WHERE pcn = ? and report_date = ?
  '''.replace('\n', ' ')

  rowcount=cursor2.execute(sql, (pcn,report_date)).rowcount
  print_to_stdout(f"{sql} - rowcount={rowcount}")
  print_to_stdout(f"{sql} - messages={cursor2.messages}")
  cursor2.commit()

  im2 ='''
  insert into DailyMetrics.daily_shift_report 
  (pcn,report_date,workcenter_key,workcenter_code,part_key,part_no,part_revision,
   part_name,operation_no,operation_code,parts_produced,parts_scrapped,
   earned_hours,actual_hours,part_operation_key,quantity_produced,labor_rate)
  values (?,?,?,?,?, ?,?,?,?,?, ?,?,?,?,?, ?,?)'''

  # test = rec[0:500]
  cursor2.fast_executemany = True
  cursor2.executemany(im2,rec) 
  # cursor2.executemany(im2,rec[13:14]) 
  cursor2.commit()
  cursor2.close()

  conn3 = mysql.connector.connect(user=username3, password=password3,
                          host='10.1.0.116',
                          port='31008',
                          database='Plex')

  cursor3 = conn3.cursor()

  sql ='''
  delete from DailyMetrics.daily_shift_report
  WHERE pcn = %s and report_date = %s
  '''.replace('\n', ' ')

  cursor3.execute(sql,(pcn,report_date))
  print_to_stdout(f"{sql} - rowcount={cursor3.rowcount}")
  conn3.commit()

  # https://github.com/mkleehammer/pyodbc/wiki/Cursor
  # https://github.com/mkleehammer/pyodbc/wiki/Features-beyond-the-DB-API#fast_executemany
  # https://towardsdatascience.com/how-i-made-inserts-into-sql-server-100x-faster-with-pyodbc-5a0b5afdba5

  im2 ='''
  insert into DailyMetrics.daily_shift_report 
  (pcn,report_date,workcenter_key,workcenter_code,part_key,part_no,part_revision,
   part_name,operation_no,operation_code,parts_produced,parts_scrapped,
   earned_hours,actual_hours,part_operation_key,quantity_produced,labor_rate)
  values (%s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s,%s,%s,%s, %s,%s)
  '''.replace('\n',' ')

  cursor3.executemany(im2,rec)
  # cursor2.executemany(im2,records_to_insert)
  conn3.commit()
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
