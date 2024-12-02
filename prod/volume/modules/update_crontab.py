#!/usr/bin/env python

#!/miniconda/bin/python # for docker image
#!/miniconda/bin/python
#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python # for debugging
#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python
# https://docs.python-zeep.org/en/master/
import pyodbc 
from datetime import datetime
import sys 
import mysql.connector
from mysql.connector import Error
import os
import json
import shutil

#%DEV%CronTab_path = '/home/brent/src/Reporting/prod/volume/CronTab'   
CronTab_path = '/volume/CronTab'   
#%DEV%ReportQueue_path = '/home/brent/src/Reporting/prod/volume/ReportQueue'   
ReportQueue_path = '/volume/ReportQueue'   

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

def update_crontab():
  try:
      print_to_stdout(f"Start of update_crontab")
      # DEBUG ONLY
      # report_id = 1
      # etl_only = 1
      # parameters = '{"etl_only":0,"report_name":"daily_metrics","email":"bgroves@buschegroup.com","start_period":202201,"end_period":202207}'
      
#      %DEV%os.environ['MYSQL_HOST'] = 'reports31'
#      %DEV%os.environ['MYSQL_PORT'] = '30031'
      
      
      # https://geekflare.com/calculate-time-difference-in-python/
      start_time = datetime.now()
      end_time = datetime.now()

      current_time = start_time.strftime("%H:%M:%S")
      print_to_stdout(f"Current Time: {current_time}")

      ret = 0

      # copy crontab template base file to new crontab-reports file
      # https://builtin.com/data-science/copy-a-file-with-python

      src =  CronTab_path + '/crontab-base' 
#      %DEV%src =  CronTab_path + '/crontab-base-dev' 
      dest =  CronTab_path + '/crontab-reports' 
      shutil.copy(src, dest)

  # https://www.pythontutorial.net/python-basics/python-read-text-file/
      with open('/etc/db-user-pass/username3') as f:
          username3 = f.read().strip()
          print_to_stdout(f'username3={username3}')

      with open('/etc/db-user-pass/password3') as f:
          password3 = f.read().strip()    
          print_to_stdout(f'password3={password3}')



      mysql_host = os.getenv('MYSQL_HOST') # None
      mysql_port = os.environ.get('MYSQL_PORT') # None

      conn3 = mysql.connector.connect(user=username3, password=password3,
                                host=mysql_host,
                                port=mysql_port,
                                database='Report')

      cursor3 = conn3.cursor()
      # https://code.google.com/archive/p/pyodbc/wikis/GettingStarted.wiki
      # https://github.com/mkleehammer/pyodbc/wiki/Cursor
# thank you Father for this work!
# get Report.crontab
# add each job to crontab file.
# https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-select.html
      sql=f'select crontab_id,job_name,params,on_hold,created,updated from Report.crontab where on_hold = 0'
      rowcount=cursor3.execute(sql)
      # head_rows = cursor.fetchmany(size=2)
      # rows = cursor3.fetchall()
      # Append-adds at last
      file1 = open(dest, "a")  # append mode
      for (crontab_id,job_name,params,on_hold,created,updated) in cursor3:
        # https://www.programiz.com/python-programming/datetime/strftime
          params_dict=json.loads(params)
          print("{},{},{},{} was created on {:%d %b %Y}".format(crontab_id,job_name,params_dict['frequency'],on_hold,created,updated))
          line ="{} cd {} && ./InsertQueue.sh".format(params_dict['frequency'],ReportQueue_path)
          file1.write(line + '\n')
      file1.write('\n')                       

        # print("{}, {} was hired on {:%d %b %Y}".format(
        #   last_name, first_name, hire_date))
      #     file1.write("Today \n")
      file1.close()
 

  # 1. pull from Report.crontab
  # 2. create a crontab file from dest
  # https://www.geeksforgeeks.org/python-append-to-a-file/

  # AT END RUN crontab /app/etl/CronTab/crontab

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
      if 'conn' in globals():
          conn.close()
      if 'conn2' in globals():
          conn2.close()
      if 'conn3' in globals():
          if conn3.is_connected():
              conn3.close()
              # print("MySQL connection is closed")
      # sys.exit(ret)

if __name__ == '__main__':
  update_crontab()
