#!/usr/bin/python
# https://blog.devgenius.io/how-to-deploy-rest-api-application-using-mysql-on-the-kubernetes-cluster-4c806de1a48
import os
from flask import Flask
from peewee import MySQLDatabase, IntegerField
from mysql.connector import Error

 
MYSQL_ROOT_USER = os.getenv('MYSQL_ROOT_USER', 'root')
MYSQL_ROOT_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD', 'password')
MYSQL_ROOT_HOST = os.getenv('MYSQL_ROOT_HOST', '10.1.0.116')
MYSQL_ROOT_PORT = os.getenv('MYSQL_ROOT_PORT', '31008')
MYSQL_ROOT_DB = os.getenv('MYSQL_ROOT_DB', 'Plex')
FLASK_APP_PORT = os.getenv('FLASK_APP_PORT', '8282')

# db = MySQLDatabase(database=MYSQL_ROOT_DB, user=MYSQL_ROOT_USER, password=MYSQL_ROOT_PASSWORD,
#                 host=MYSQL_ROOT_HOST, port=int(MYSQL_ROOT_PORT))
# cursor = db.cursor()
# cursor.execute("SELECT VERSION()")
# data = cursor.fetchone()

 
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
 
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'
 
# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()

# db = MySQLDatabase(database=MYSQL_ROOT_DB, user=MYSQL_ROOT_USER, password=MYSQL_ROOT_PASSWORD,
#                 host=MYSQL_ROOT_HOST, port=int(MYSQL_ROOT_PORT))

# app = Flask(__name__)
# app.run(host='0.0.0.0', port=int(FLASK_APP_PORT))


# @app.route('/')
# def get_db_version():
#     try:
#         return "Hello"
#         # cursor = db.cursor()
#         # cursor.execute("SELECT VERSION()")
#         # data = cursor.fetchone()
#         # db.close()
#         # return "Database version : %s " % data
#     except Error as e:
#         print("Error while connecting to MySQL", e)

#     except BaseException as error:
#         print('An exception occurred: {}'.format(error))
#     finally:
#         print("done")
