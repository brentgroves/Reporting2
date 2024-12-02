#!/miniconda/bin/python 

#!/miniconda/bin # for docker image
#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python # for debugging
# https://docs.python-zeep.org/en/master/
#####!/usr/bin/env python

#import xmltodict
from zeep import Client
from requests import Session
from requests.auth import HTTPBasicAuth  # or HTTPDigestAuth, or OAuth1, etc.
from zeep.transports import Transport
import pyodbc
import logging.config
import sys 

def print_to_stdout(*a):
 
    # Here a is the array holding the objects
    # passed as the argument of the function
    print(*a, file = sys.stdout)

def print_to_stderr(*a):
 
    # Here a is the array holding the objects
    # passed as the argument of the function
    print(*a, file = sys.stderr)
 

# https://docs.python-zeep.org/en/master/transport.html?highlight=authentication#http-authentication
session = Session()
session.auth = HTTPBasicAuth('MGEdonReportsws@plex.com','9f45e3d-67ed-')

client = Client(wsdl='../wsdl/Plex_SOAP_test.wsdl',transport=Transport(session=session))
# https://docs.python-zeep.org/en/master/datastructures.html
e_type = client.get_type('ns0:ExecuteDataSourceRequest')
a_ip_type = client.get_type('ns0:ArrayOfInputParameter')
ip_type=client.get_type('ns0:InputParameter')
Report_Date=ip_type(Value='2022-04-28 08:00:00',Name='@Report_Date',Required=False,Output=False)
End_Date=ip_type(Value='2022-04-28 08:59:59',Name='@End_Date',Required=False,Output=False)


Parameters=a_ip_type([Report_Date,End_Date])

e=e_type(DataSourceKey=8619,InputParameters=Parameters,DataSourceName='Detailed_Production_Get_New')


response = client.service.ExecuteDataSource(e)

result = response['ResultSets'].ResultSet[0].Rows.Row
length=len(result)

list = response['ResultSets'].ResultSet[0].Rows.Row
# print("Length=% s" % len(list))

# Using for loop
for i in list:
    column_names=""
    column_values=""
    dic ={}
    ind=0
    for j in i.Columns.Column:
      column_names=column_names+j.Name+','
      if j.Value is None:
        column_values=column_values+','  
      else:
        column_values=column_values+j.Value+','
      dic.update({j.Name:ind}) 
      ind=ind+1

rs = response['ResultSets'].ResultSet[0].Rows.Row[0]
PCN = 306766
rec=[]
for i in list:
  rec.append((PCN,i.Columns.Column[18].Value,i.Columns.Column[1].Value,i.Columns.Column[2].Value,i.Columns.Column[9].Value))

try:
  ret = 0


  username = 'mgadmin' 
  password = 'BadPassword' 
  # password = 'WeDontSharePasswords1!' 
  conn = pyodbc.connect('DSN=dw;UID='+username+';PWD='+ password + ';DATABASE=mgdw')

  cursor = conn.cursor()

  ins ='''insert into Validation.Detailed_Production_History (pcn,production_no,part_no,part_key,record_date)
  values (?,?,?,?,?)'''
  print_to_stdout(ins)


  cursor.executemany(ins,rec)
# https://towardsdatascience.com/how-i-made-inserts-into-sql-server-100x-faster-with-pyodbc-5a0b5afdba5

except pyodbc.Error as ex:
  ret = 1
  # print('exception')
  print_to_stdout("std out message") 
  print_to_stderr("ODBC connection error.") 

finally:
  if 'cursor' in globals():
    cursor.commit()
    cursor.close()
  if 'conn' in globals():
    conn.close()
  sys.exit(ret)

# #python -mzeep Plex_SOAP_test.wsdl
# # https://www.youtube.com/watch?v=JBYEQjg_znI
