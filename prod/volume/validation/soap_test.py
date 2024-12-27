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
  pcn = '123681'
    # pcn = '300758'
  username = 'mg.odbcalbion'
  password = 'Mob3xalbion'
  username2 = 'mgadmin' 
  password2 = 'WeDontSharePasswords1!' 
  username3 = 'root'
  password3 = 'password'
  username4 = 'MGEdonReportsws@plex.com'
  password4 = '9f45e3d-67ed-'
  mysql_host = 'reports31'
    # mysql_host = 'reports13'
  mysql_port = '30031'
  azure_dw = '1'


  # https://geekflare.com/calculate-time-difference-in-python/
  start_time = datetime.now()
  end_time = datetime.now()

  current_time = start_time.strftime("%H:%M:%S")
  print_to_stdout(f"Current Time: {current_time=}")

  start_period = 0
  end_period = 0
  start_open_period = 202410
  end_open_period = 202410
  no_update = 9


  period = start_open_period

  year = period // 100



  # https://docs.python-zeep.org/en/master/transport.html?highlight=authentication#http-authentication
  session = Session()
  session.auth = HTTPBasicAuth(username4,password4)
  # session.auth = HTTPBasicAuth('MGEdonReportsws@plex.com','9f45e3d-67ed-')

  client = Client(wsdl='/home/brent/src/Reporting2/prod/volume/wsdl/Plex_SOAP_prod.wsdl',transport=Transport(session=session)) # prod
#client = Client(wsdl='/home/brent/src/Reporting2/prod/volume/wsdl/Plex_SOAP_prod.wsdl',transport=Transport(session=session)) # stand-alone .
  
  # https://docs.python-zeep.org/en/master/datastructures.html
  e_type = client.get_type('ns0:ExecuteDataSourceRequest')
  a_ip_type = client.get_type('ns0:ArrayOfInputParameter')
  ip_type=client.get_type('ns0:InputParameter')
  ip_pcn = ip_type(Value=pcn,Name='@PCNs',Required=False,Output=False)


  # account_no_from and account_no_to parameters are inclusive
  # Account total from accounting_account_DW_Import on Dec 3,2024 = 4889
  # Try to break accounts into 2 groups of ~ 2500 records
  # to prevent web service call from timing out.

  # Total records = 2209 + 2684 = 4893
  # row_count = 2209 on Dec 3, 2024
  # account_no_from = '00000-000-0000'
  # account_no_to = '66666-666-6666'

  # # row_count = 2684 on Dec 3, 2024
  # account_no_from = '66666-666-6666'
  # account_no_to = '99999-999-9999'

  account_no_from = '11010-000-0000'
  account_no_to = '11010-000-0000'

  ip_period_start = ip_type(Value=period,Name='@Period_Start',Required=True,Output=False)
  ip_period_end = ip_type(Value=period,Name='@Period_End',Required=True,Output=False)
  ip_account_no_from = ip_type(Value=account_no_from,Name='@Account_No_From',Required=False,Output=False)
  ip_account_no_to = ip_type(Value=account_no_to,Name='@Account_No_To',Required=False,Output=False)
  Parameters=a_ip_type([ip_pcn,ip_period_start,ip_period_end,ip_account_no_from,ip_account_no_to])

  # e=e_type(DataSourceKey=8619,InputParameters=[{'Value':'4/26/2022','Name':'@Report_Date','Required':False,'Output':False}],DataSourceName='Detailed_Production_Get_New')
  e=e_type(DataSourceKey=4814,InputParameters=Parameters,DataSourceName='Account_Activity_Summary_xPCN_Get')

  test=0
  response = client.service.ExecuteDataSource(e)

  test=0
  if response.Error == True:
    test=1
  if response.Error == False:
    test=2

  # collect desired columns of the result set into a list  
  list = response['ResultSets'].ResultSet[0].Rows.Row
  rec=[]
  row=0

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