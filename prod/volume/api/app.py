# https://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api
# The Web Server Gateway Interface (WSGI, pronounced whiskey or WIZ-ghee)
#  is a simple calling convention for web servers to forward requests to 
# web applications or frameworks written in the Python programming language.
import email
from flask import Flask, request
from flask_restful import Resource, abort, Api, reqparse
from marshmallow import Schema, fields
from marshmallow import ValidationError
import trial_balance.parameters  as trial_balance_parameters
import mean_time_between_failues.parameters as mean_time_between_failures_parameters
import daily_metrics.parameters as daily_metrics_parameters
import os
import subprocess
import sys
import json
# from jsonschema import validate
# https://www.geeksforgeeks.org/python-import-module-outside-directory/
# import ReportQueue.insert as insert # this did not work from code debug.
# inserting the mod.py directory at
# position 1 in sys.path
sys.path.insert(1, '/home/brent/src/Reporting/prod/etl/modules')   
import report_queue
import report_crontab

app = Flask(__name__)
api = Api(app)

def print_to_stdout(*a):
    # Here a is the array holding the objects
    # passed as the argument of the function
    print(os.path.basename(__file__)+':',*a, file = sys.stdout)


def print_to_stderr(*a):
    # Here a is the array holding the objects
    # passed as the argument of the function
    print(os.path.basename(__file__)+':',*a, file = sys.stderr)

class ReportList(Resource):
# Get
    # curl http://localhost:5000/report_list
    def get(self):
        return "trial_balance,daily_metrics,mean_time_between_failures"

# Thank you, Father for the work that you give us.
api.add_resource(ReportList, '/report_list')

class Report(Resource):
# Get
    # curl http://localhost:5000/report/trial_balance
    def get(self,report_name):
        # return_value = os.system('ls -l')
        # print(f"return_value={return_value}")
        # return_value = os.system('ls -l')
        # print(f"return_value={return_value}")
        return_value = ''

        if report_name == "trial_balance":
            return_value = """curl -k -X POST https://reports01/report -H 'Content-Type: application/json' -d '{"report_name":"trial_balance","email":"username@buschegroup.com","start_period":202201,"end_period":202207}' Please replace the single quotes with double quotes.""" 
            # return_value = """curl -k -X POST https://reports01/report -H \"Content-Type: application/json\" -d \"{"report_name":"trial_balance","email":"username@buschegroup.com","start_period":202201,"end_period":202207}\"""" 
        elif report_name == "daily_metrics":
            return_value = """curl -X POST http://reports01/report -H 'Content-Type: application/json' -d '{"report_name":"daily_metrics","email":"username@buschegroup.com","start_period":202201,"end_period":202207}' Please remove all the backslashes and replace username@buschegroup.com with your username."""     
        elif report_name == "mean_time_between_failures":
            return_value = """curl -X POST http://reports01/report -H 'Content-Type: application/json' -d '{"report_name":"mean_time_between_failures","email":"username@buschegroup.com","start_period":202201,"end_period":202207}' Please remove all the backslashes and replace username@buschegroup.com with your username."""     
        return return_value
# Post    
    # curl -X POST http://localhost:5000/report -H 'Content-Type: application/json' -d '{"report_name":"trial_balance","email":"username@buschegroup.com","start_period":202201,"end_period":202207}'
    # curl -X POST http://localhost:5000/report -H 'Content-Type: application/json' -d '{"job_name":"trial_balance.open_periods.dm.daily","report_name":"trial_balance","email":"username@buschegroup.com","start_period":202201,"end_period":202207}'
    def post(self):
        try:
            parameters = request.get_json()
            if "report_name" not in parameters:
                error_msg = """Please check command syntax it should look like this except the single quotes need to be replaced with double quotes: curl -k -X POST https://reports01/report -H 'Content-Type: application/json' -d '{"report_name":"trial_balance","email":"username@buschegroup.com","start_period":202201,"end_period":202207}'""" 
                raise Exception(error_msg)
            report_name=parameters['report_name']
            if report_name == "trial_balance":
                parameters_dict = trial_balance_parameters.parameters.load(request.get_json())
                if 'frequency' not in parameters_dict.keys():
                    parameters_dict['frequency'] = 'once'
                if 'etl_only' not in parameters_dict.keys():
                    parameters_dict['etl_only'] = 0
                # Thank you Father for the work you have blessed us with!
                # Please continue to direct us in your plan.
                etl_only=str(parameters_dict['etl_only'])
                email=parameters_dict['email']
                start_period=str(parameters_dict['start_period'])
                end_period=str(parameters_dict['end_period'])
                frequency=parameters_dict['frequency']
                params=f'{{"etl_only":{etl_only},"report_name":"{report_name}","email":"{email}","start_period":{start_period},"end_period":{end_period}}}'
                if frequency == 'once':                
                    report_queue.insert_queue(params=params)
                elif "job_name" not in parameters:
                    error_msg = """Please check command syntax it should look like this except the single quotes need to be replaced with double quotes: curl -k -X POST https://reports01/report -H 'Content-Type: application/json' -d '{"report_name":"trial_balance","email":"username@buschegroup.com","start_period":202201,"end_period":202207}'""" 
                    raise Exception(error_msg)

                    report_crontab.insert_crontab(job_name,)
                # report_queue.insert_queue(params='{"etl_only":0,"report_name":"daily_metrics","email":"bgroves@buschegroup.com","start_period":202201,"end_period":202207}')


            elif report_name == "daily_metrics":
                parameters_dict = daily_metrics_parameters.parameters.load(request.get_json())
            elif report_name == "mean_time_between_failures":
                parameters_dict = mean_time_between_failures_parameters.parameters.load(request.get_json())
            else:
                raise Exception("Invalid report_name the choices are: trial_balance")

        # https://janakiev.com/blog/python-shell-commands/
        except Exception as e:
            return e.args[0], 422
        except json.decoder.JSONDecodeError:
            error_msg = """Invalid command syntax:\ncurl -k -X POST https://reports01/report -H 'Content-Type: application/json' -d '{"report_name":"trial_balance","email":"username@buschegroup.com","start_period":202201,"end_period":202207}' Formatting Issue: Please replace the single quotes with double quotes and remove the double quotes enclosing this command.""" 
            return error_msg, 422
        except ValidationError as err:
            return err.messages, 422
        if etl_only=='1':    
            msg = f"The job with the following parameters has been added to crontab:{parameters_dict['report_name']},email:{parameters_dict['email']},start_period:{parameters_dict['start_period']},end_period:{parameters_dict['end_period']}"
        else:
            msg = f"Report in progress expect email within 10 minutes for report_name:{parameters_dict['report_name']},email:{parameters_dict['email']},start_period:{parameters_dict['start_period']},end_period:{parameters_dict['end_period']}"

        return msg 
        # return f"curl -k -X POST https://reports01/report -H 'Content-Type: application/json' -d \'{{"report_name":"trial_balance","email":"username@buschegroup.com","start_period":202201,"end_period":202207}}'" 

        # return f"Report in progress for report_name:{parameters_dict['report_name']},email:{parameters_dict['email']},start_period:{parameters_dict['start_period']},end_period:{parameters_dict['end_period']}"
        # return 'report in progress... email will be sent shortly.' 

# Thank you, Father for the work that you give us.
api.add_resource(Report, '/report/<string:report_name>','/report')

# https://stackoverflow.com/questions/34457981/trying-to-run-flask-app-gives-address-already-in-use
# app.run() is ignored in visual code. see launch.json to change variables
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5001)
