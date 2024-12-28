#!/miniconda/bin/python
#!/usr/bin/python
import pyodbc 
# https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-1-configure-development-environment-for-pyodbc-python-development?view=sql-server-ver15
# docker run -it --name my-manim-container -v "/home/bgroves@BUSCHE-CNC.COM/srcmanim:/manim" manimcommunity/manim /bin/bash
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
# MSSQLTest
username = 'credentials' 
password = 'credentials' 
cnxn = pyodbc.connect('DSN=Plex;UID='+username+';PWD='+ password)
#cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
#Sample select query
cursor.execute("select count(*) from accounting_v_account;") 
row = cursor.fetchone() 
while row: 
    print(row[0])
    row = cursor.fetchone()
