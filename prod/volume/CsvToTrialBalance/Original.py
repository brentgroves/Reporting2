#!/usr/bin/env python

#!/miniconda/bin/python
#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python
#!/miniconda/bin/python # for docker image
#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python # for debugging
# https://www.webtrainingroom.com/python/excel-to-mysql-using-python
# https://linchpiner.github.io/k8s-multi-container-pods.html#:~:text=Why%20does%20Kubernetes%20allow%20more,efficiently%20communicate%2C%20ensuring%20data%20locality.
# https://gist.github.com/madan712/b01e85eeddecf9b92b53f8d3e11986d7
# https://www.webtrainingroom.com/python/excel-to-mysql-using-python
# https://medium.com/analytics-vidhya/import-data-from-excel-into-mysql-using-python-c80c2bd8676a#id_token=eyJhbGciOiJSUzI1NiIsImtpZCI6ImFmYzRmYmE2NTk5ZmY1ZjYzYjcyZGM1MjI0MjgyNzg2ODJmM2E3ZjEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYmYiOjE2NzUxOTAxODEsImF1ZCI6IjIxNjI5NjAzNTgzNC1rMWs2cWUwNjBzMnRwMmEyamFtNGxqZGNtczAwc3R0Zy5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjExMzc3MDA0NjA0MzIxMDE1MTI1MiIsImVtYWlsIjoiYnJlbnQuZ3JvdmVzQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhenAiOiIyMTYyOTYwMzU4MzQtazFrNnFlMDYwczJ0cDJhMmphbTRsamRjbXMwMHN0dGcuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJuYW1lIjoiYnJlbnQgZ3JvdmVzIiwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FFZEZUcDYyRG15dEwtNUYtc0V5dC10YTNRTk5NRzhGLVdhZ3A2dnN3bFVkPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6ImJyZW50IiwiZmFtaWx5X25hbWUiOiJncm92ZXMiLCJpYXQiOjE2NzUxOTA0ODEsImV4cCI6MTY3NTE5NDA4MSwianRpIjoiMWJkMDlkZDVkMGE5ZTgyNTkxNTMzNjFiODE2YzFkN2QxNmNhMTE0ZiJ9.dmg21MiMV3jsmACJg74KySYTZiWgQZDcZUZMRAZs7aDGk7_PINRQcqmo3AyHBn5wy3MGPJDCA7ocfxVmgIHOiGE4NFjUh0eDASxENIPU-QxbBpVbBLjgopNcICvFZ5UX_bFuYZ8rEJQJAY5lLZG2loxzXNdocvrfZUdQBWm-9qEuNZxhobHAsDMb2FLCguEwIb2jIzYFm2E2CHN1ue9AoaAwoee2kPVfK-PTbzFoV_ztQ4pRWdCxYP05yZX18McEM1swZqSGfYub9wXCTZuyeW2vvRWXY4Rl09RLKppi40Q0FYigHZB3Mqscy2CQRso8YXZmA13iJa-pIdivwC-Nsg
import pyodbc 
from datetime import datetime
import sys 
import mysql.connector
from mysql.connector import Error
import os
import xlsxwriter

# https://www.justintodata.com/send-email-using-python-tutorial/
# https://medium.com/@neonforge/how-to-send-emails-with-attachments-with-python-by-using-microsoft-outlook-or-office365-smtp-b20405c9e63a
# Import modules
import smtplib
## email.mime subclasses
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
### Add new subclass for adding attachments
##############################################################
from email.mime.application import MIMEApplication
##############################################################
## The pandas library is only for generating the current date, which is not necessary for sending emails
import pandas as pd
# import os.path


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
    print(os.path.basename(__file__)+':',*a, file = sys.stdout)


def print_to_stderr(*a):
    # Here a is the array holding the objects
    # passed as the argument of the function
    print(os.path.basename(__file__)+':',*a, file = sys.stderr)


# Define the HTML document
html = '''
    <html>
        <body>
            <h1>Trial Balance report</h1>
            <p>Hello, welcome to your report!</p>
        </body>
    </html>
    '''

# Define a function to attach files as MIMEApplication to the email
##############################################################
def attach_file_to_email(email_message, filename):
    # Open the attachment file for reading in binary mode, and make it a MIMEApplication class
    with open(filename, "rb") as f:
        file_attachment = MIMEApplication(f.read())
    filename_only = os.path.basename(filename)    
    # Add header/name to the attachments    
    file_attachment.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename_only}",
    )
    # Attach the file to the message
    email_message.attach(file_attachment)
##############################################################    

try:
    ret = 0
    pcn = (sys.argv[1])
    username3 = (sys.argv[2])
    password3 = (sys.argv[3])
    mysql_host = (sys.argv[4])
    mysql_port = (sys.argv[5])
    start_period = (sys.argv[6])
    end_period = (sys.argv[7])
    email_from = 'mcp@buschegroup.com'
    email_to = (sys.argv[8])


    # pcn = '300758'
    # pcn = '123681'
    # username3 = 'root'
    # password3 = 'password'   
    # mysql_host = 'reports03'
    # # mysql_host = 'reports13'
    # mysql_port = '31008'
    # start_period = 202209
    # end_period = 202209
    # email_from = 'mcp@buschegroup.com'
    # email_to = 'bgroves@buschegroup.com'

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

    # https://geekflare.com/calculate-time-difference-in-python/
    start_time = datetime.now()
    end_time = datetime.now()

    current_time = start_time.strftime("%Y-%m-%d_%H-%M-%S")
    print_to_stdout(f"Current Time: {current_time=}")

    filename = f"TrialBalance-{current_time}.xlsx"

    # Production
    os.chdir('/app/output')
    # Development
    # os.chdir('/home/bgroves@BUSCHE-CNC.COM/src/Reporting/output')

    # Create an new Excel file and add a worksheet.
    workbook = xlsxwriter.Workbook(filename)
    # workbook = xlsxwriter.Workbook(filename + '.xlsx')
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

    # cursor3.commit()
    cursor3.close()


    # Generate today's date to be included in the email Subject
    date_str = pd.Timestamp.today().strftime('%Y-%m-%d')

    # Create a MIMEMultipart class, and set up the From, To, Subject fields
    email_message = MIMEMultipart()
    email_message['From'] = email_from
    email_message['To'] = email_to
    email_message['Subject'] = f'Trial Balance Report - {date_str}'

    # Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
    email_message.attach(MIMEText(html, "html"))

    # Attach more (documents)
    cwd = os.getcwd()
    full_filename = cwd + '/' + filename
    ##############################################################
    # attach_file_to_email(email_message, '/home/bgroves@BUSCHE-CNC.COM/src/python-train/how_to/smtp/github.png')
    attach_file_to_email(email_message, full_filename)
    # attach_file_to_email(email_message, '/home/bgroves@BUSCHE-CNC.COM/src/python-train/how_to/smtp/dsp.pdf')
    ##############################################################
    # Convert it as a string
    email_string = email_message.as_string()

    with smtplib.SMTP('mobexglobal-com.mail.protection.outlook.com') as server:
        server.sendmail(email_from, email_to, email_string) 

    fetch_time = datetime.now()
    tdelta = fetch_time - start_time 
    print_to_stdout(f"fetch_time={tdelta}") 

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
