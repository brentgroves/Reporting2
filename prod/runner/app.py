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
    # DEBUG ONLY
    os.environ['MYSQL_HOST'] = 'reports31'
    os.environ['MYSQL_PORT'] = '30031'

    # https://geekflare.com/calculate-time-difference-in-python/
    start_time = datetime.now()
    end_time = datetime.now()

    current_time = start_time.strftime("%H:%M:%S")
    print_to_stdout(f"Current Time: {current_time}")

    ret = 0

# https://www.pythontutorial.net/python-basics/python-read-text-file/
    with open('/etc/foo/username3') as f:
        username3 = f.read().strip()
        print(f'username3={username3}')

    with open('/etc/foo/password3') as f:
        password3 = f.read().strip()    
        print(f'password3={password3}')



    # Getting non-existent keys
    mysql_host = os.getenv('MYSQL_HOST') # None
    mysql_port = os.environ.get('MYSQL_PORT') # None

    conn3 = mysql.connector.connect(user=username3, password=password3,
                              host=mysql_host,
                              port=mysql_port,
                              database='Report')

    cursor3 = conn3.cursor()
    # https://code.google.com/archive/p/pyodbc/wikis/GettingStarted.wiki
    # https://github.com/mkleehammer/pyodbc/wiki/Cursor

    sql='select queue_id,report_id,parameters,done,created,updated from Report.queue where done = 0 order by queue_id limit 1'
    rowcount=cursor3.execute(sql)
    if rowcount is not None:
        row = cursor3.fetchone()
        report = { 
            'queue_id':row[0],
            'report_id':row[1],
            'parameters':row[2],
            'created':row[3],
            'updated':row[4]
        }
        print_to_stdout(f"report: {report}")
        print_to_stdout(f"report: {report['parameters']}")
      # aDict = json.loads(jsonString)
        params = json.loads(report['parameters'])
        report_name=params['report_name']
        frequency=params['frequency']
        # Thank you Father for the work you have blessed us with!
        # Please continue to direct us in your plan.
        if report_name == "trial_balance":
            # Production
            # os.chdir('/app/etl/PipeLine')
            # Production testing
            os.chdir('/home/brent/src/Reporting/prod/etl/PipeLine')
            # Development
            # os.chdir('/home/brent/src/Reporting/dev/etl/PipeLine')
            # file_name = './TrialBalance.sh'
            file_name = './TrialBalanceDocker.sh'
            # file_name = './TrialBalanceValidate.sh'
            # Parameters needed for trial balance report:
            # report_name = 'trial_balance'
            # email = "bgroves@buschegroup.com"
            # start_period = '202208'
            # end_period = '202208'
            # frequency = 'once'
            etl_only=params['etl_only']
            if params['etl_only'] == 1:
              email='na'
              start_period='na'
              end_period='na'
            else:
              email=params['email']
              start_period=str(params['start_period'])
              end_period=str(params['end_period'])

            cmd = file_name + ' ' + report_name + ' ' + etl_only + ' ' + email + ' ' + start_period + ' ' + end_period 

            print(f'cmd={cmd}')
            result=0
             # Using universal_newlines=True converts the output to a string instead of a byte array.
            result = subprocess.Popen(cmd, shell=True)
            print(f'\nFrom app.py -> result={result}')

        sql=f"update Report.queue set done=1 where queue_id={report['queue_id']}"
        cursor3.execute(sql)
        conn3.commit()

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
