# https://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api
# https://ch-rowley.github.io/2021/10/24/How-to-marshal-data-with-Flask.html
# https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html
# https://curl.se/docs/manpage.html#-k
import email
# from lib2to3.pytree import BasePattern
from flask import Flask, request
from flask_restful import Resource, abort, Api, reqparse
from marshmallow import Schema, fields
from marshmallow import ValidationError
import trial_balance.parameters  as trial_balance_parameters
import mean_time_between_failues.parameters as mean_time_between_failures_parameters
import daily_metrics.parameters as daily_metrics_parameters
import os
import subprocess

app = Flask(__name__)
api = Api(app)

# class Parameters(Schema):
#     report_name = fields.Str(required=True)
#     email = fields.Email(required=True)
#     start_period = fields.Int(required=True)
#     end_period = fields.Int(required=True)

# parameters = Parameters()

class ReportList(Resource):
# Get
    # curl http://localhost:5000/report_list
    def get(self):
        print(f'In ReportList.get')
        # Popen does not wait for the shell to complete so is better for 
        # rest api
        os.chdir('/home/bgroves@BUSCHE-CNC.COM/src/Reporting/dev/api/run_shell_commands')
        # Using universal_newlines=True converts the output to a string instead of a byte array.
        # If shell=True, the command string is interpreted as a raw shell command.
        file_name = './main.sh'
        # Parameters needed for trial balance report
        # "report_name":"trial_balance","email":"username@buschegroup.com",
        # "start_period":202201,"end_period":202207}' Formatting Issue: Please replace the single quotes with double quotes and remove the double quotes enclosing this command.""" 

        report_name = 'trial_balance'
        email = "bgroves@buschegroup.com"
        start_period = '202108'
        end_period = '202208'
        frequency = 'once'
        cmd = file_name + ' ' + report_name + ' ' + email + ' ' + start_period + ' ' + end_period + ' ' + frequency
        print(f'cmd={cmd}')
        result = subprocess.Popen(cmd, shell=True)
        # result = subprocess.Popen('./main.sh', shell=True)
        print(f'\nFrom run_shell_command.py -> result={result}')

        # # This only prints the return code of the command
        # # If you save this as a script and run it, you will see the output in the command line. 
        # # The problem with this approach is in its inflexibility since you can’t even get the resulting output as a variable. 
        # # You can read more about this function in the documentation.
        # print(os.system('printf "PATH=$PATH"'))

        # os.system('echo $HOME > outfile')
        # f = open('outfile','r')
        # print(f.read())

        # # stream = os.popen('echo Returned output')
        # # output = stream.read()
        # # stream.close()
        # stream = os.popen('echo Returned output',mode='r')
        # output = stream.readline()
        # output = output + ".  Append this to output"
        # print(output)

        # print(os.system('pwd'))
        # os.chdir('/home/bgroves@BUSCHE-CNC.COM/src/Reporting/dev/api/run_shell_commands')
        # print(os.system('pwd'))


        # subprocess.call(['ls','-l'])
        # # The command line arguments are passed as a list of strings, which avoids the need for escaping quotes or other special characters 
        # # that might be interpreted by the shell.

        # # $PATH error no such file or directory because no shell expansion
        # # subprocess.call('echo $PATH')

        # subprocess.call('echo $PATH', shell=True)

        # # Setting the shell argument to a true value causes subprocess to spawn an intermediate shell process, and tell it to run the command. 
        # # In other words, using an intermediate shell means that variables, glob patterns, and other special shell features in the command string 
        # # are processed before the command is run. Here, in the example, $HOME was processed 
        # # before the echo command. Actually, this is the case of command with shell expansion while the command ls -l considered as a simple command.
        # result = subprocess.call('./main.sh', shell=True)
        # print(f'\nFrom run_shell_command.py -> result={result}')

        return "trial_balance,daily_metrics,mean_time_between_failures"

# Thank you, Father for the work that you give us.
api.add_resource(ReportList, '/report_list')

class Report(Resource):
# Get
    # curl http://localhost:5000/report/trial_balance
    def get(self,report_name):
        return_value = os.system('ls -l')
        print(f"return_value={return_value}")
        # return_value = os.system('ls -l')
        # print(f"return_value={return_value}")
        return_value = ''
# https://everything.curl.dev/usingcurl/verbose/writeout
# curl -w "Type: %{content_type}\nCode: %{response_code}\n" http://localhost:5000/report/trial_balance
        if report_name == "trial_balance":
            # return_value = "''''"
            return_value = """curl -k -X POST https://reports01/report -H 'Content-Type: application/json' -d '{"report_name":"trial_balance","email":"username@buschegroup.com","start_period":202201,"end_period":202207}' Formatting Issue: Please replace the single quotes with double quotes and remove the double quotes enclosing this command.""" 
            # return_value = """curl -X POST http://reports01/report -H 'Content-Type: application/json' -d '{"report_name":"trial_balance","email":"username@buschegroup.com","start_period":202201,"end_period":202207}' Please remove all the backslashes and replace username@buschegroup.com with your username."""     
        elif report_name == "daily_metrics":
            return_value = """curl -X POST http://reports01/report -H 'Content-Type: application/json' -d '{"report_name":"daily_metrics","email":"username@buschegroup.com","start_period":202201,"end_period":202207}' Please remove all the backslashes and replace username@buschegroup.com with your username."""     
        elif report_name == "mean_time_between_failures":
            return_value = """curl -X POST http://reports01/report -H 'Content-Type: application/json' -d '{"report_name":"mean_time_between_failures","email":"username@buschegroup.com","start_period":202201,"end_period":202207}' Please remove all the backslashes and replace username@buschegroup.com with your username."""     
        return return_value
# Post    
    # curl -X POST http://localhost:5000/report -H 'Content-Type: application/json' -d '{"report_name":"trial_balance","email":"bgroves@buschegroup.com","start_period":202108,"end_period":202208, "frequency":"once"}'
    def post(self):
        parameters = request.get_json()
        try:
            report_name=parameters['report_name']
            if report_name == "trial_balance":
                parameters_dict = trial_balance_parameters.parameters.load(request.get_json())
                if 'frequency' not in parameters_dict.keys():
                    parameters_dict['frequency'] = 'once'
# Thank you Father for the work you have blessed us with!
# Please continue to direct us in your plan.
                # rest api
                os.chdir('/home/bgroves@BUSCHE-CNC.COM/src/Reporting/dev/pipeline')
                # Using universal_newlines=True converts the output to a string instead of a byte array.
                # If shell=True, the command string is interpreted as a raw shell command.
                file_name = './TrialBalanceValidate.sh'
                # Parameters needed for trial balance report
                # "report_name":"trial_balance","email":"username@buschegroup.com",
                # "start_period":202201,"end_period":202207}' Formatting Issue: Please replace the single quotes with double quotes and remove the double quotes enclosing this command.""" 

                report_name = 'trial_balance'
                email = "bgroves@buschegroup.com"
                start_period = '202108'
                end_period = '202208'
                frequency = 'once'
                cmd = file_name + ' ' + report_name + ' ' + start_period + ' ' + end_period + ' ' + frequency
                print(f'cmd={cmd}')
                result = subprocess.Popen(cmd, shell=True)
                # result = subprocess.Popen('./main.sh', shell=True)
                print(f'\nFrom app.py -> result={result}')

                # parameters_dict['email']
            elif report_name == "daily_metrics":
                parameters_dict = daily_metrics_parameters.parameters.load(request.get_json())
            elif report_name == "mean_time_between_failures":
                parameters_dict = mean_time_between_failures_parameters.parameters.load(request.get_json())

        # https://janakiev.com/blog/python-shell-commands/

        except ValidationError as err:
            return err.messages, 422
        return f"report_name:{parameters_dict['report_name']},email:{parameters_dict['email']},start_period:{parameters_dict['start_period']},end_period:{parameters_dict['end_period']}:frequency:{parameters_dict['frequency']}"
        # return 'report in progress... email will be sent shortly.' 

# Thank you, Father for the work that you give us.
api.add_resource(Report, '/report/<string:report_name>','/report')


hotels = {}
hotel_dict = {}

class HotelSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    state = fields.Str(required=True)
    rooms = fields.Int(required=True)
    start_date = fields.DateTime()


hotel_schema = HotelSchema()

def abort_if_todo_doesnt_exist(hotel_id):
    if hotel_id not in hotels:
        abort(404, message="Hotel {} doesn't exist".format(hotel_id))

class HotelList(Resource):
    # curl http://localhost:5000/hotels
    def get(self):
        return hotels

# curl -X POST http://localhost:5000/hotel -H 'Content-Type: application/json' -d '{"id":"1","name":"name1","state":"state1","rooms":"1"}'
    def post(self):
        v1 = request.get_json()
        try:
            hotel_dict = hotel_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 422

        id = hotel_dict["id"]
        hotels[id] = hotel_dict
        # new_hotel_object = Hotel(**hotel_dict)
        # return {"hotel_id": new_hotel_object.id}, 201        
        return {id: hotels[id]} 


class HotelsAPI(Resource):

# Get
    # curl http://localhost:5000/hotels/1
    def get(self, hotel_id):
        abort_if_todo_doesnt_exist(hotel_id)
        hotel = hotels[hotel_id]
        # hotel = Hotel.query.get(hotel_id)
        # return hotel_schema.dump(hotel)
        return {hotel_id: hotels[hotel_id]}
# Update
# curl http://localhost:5000/hotels/1 -d "rooms=3" -X PUT -v
# For posted form input, use request.form.
# email = request.form.get('email')
# https://stackoverflow.com/questions/10434599/get-the-data-received-in-a-flask-request
# https://flask.palletsprojects.com/en/2.2.x/api/#flask.Request
    def put(self, hotel_id):
        email = request.form.get('rooms')
        # hotels[hotel_id] = request.form['data']
        # hotels[hotel_id] = request.form['data']
        return {hotel_id: hotels[hotel_id]}
# Delete
# curl http://localhost:5000/hotel/1 -X DELETE -v
    def delete(self, hotel_id):
        abort_if_todo_doesnt_exist(hotel_id)
        del hotels[hotel_id]
        return '', 204

        # Thank you Abba for this work! Can not ouput the datetime field
api.add_resource(HotelList, '/hotel')
api.add_resource(HotelsAPI, '/hotel/<int:hotel_id>')
# api.add_resource(HotelsAPI, '/hotel','/hotel/<string:hotel_id>')

print('curl http://localhost:5000/hotel/1 -d "data=Hotel 1" -X PUT')

# curl -X POST http://localhost:5000/hotel -H 'Content-Type: application/json' -d '{"id":"1","name":"name1","state":"state1","rooms":"2"}'
# curl -X POST http://localhost:5000/hotel
#    -H 'Content-Type: application/json'
#    -d '{"id":"1"}'

todos = {}

class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

api.add_resource(TodoSimple, '/<string:todo_id>')

class Todo1(Resource):
    def get(self, todo_id):
        print(todo_id)
        # Default to 200 OK
        return {'task': 'Hello world'}

api.add_resource(Todo1, '/todo1/<string:todo_id>')

class Todo2(Resource):
    def get(self, todo_id):
        print(todo_id)
        # Set the response code to 201
        return {'task': 'Hello world'}, 201

api.add_resource(Todo2, '/todo2/<string:todo_id>')

class Todo3(Resource):
    def get(self,todo_id):
        print(todo_id)
        # Set the response code to 201 and return custom headers
        return {'task': 'Hello world'}, 201, {'Etag': 'some-opaque-string'}

api.add_resource(Todo3, '/todo3/<string:todo_id>')

class Todo4(Resource):
    def get(self,todo_id):
        print(todo_id)
        # Set the response code to 201 and return custom headers
        return {'task': 'Hello world'}, 201, {'Etag': 'some-opaque-string'}

    def put(self,todo_id):
        print(todo_id)
        parser = reqparse.RequestParser()
        parser.add_argument('rate', type=int, help='Rate to charge for this resource')
        args = parser.parse_args()        
        # Set the response code to 201 and return custom headers
        return {'task': 'Hello world'}, 201, {'Etag': 'some-opaque-string'}

api.add_resource(Todo4, '/todo4/<string:todo_id>')

print('from requests import put, get')
print("get('http://localhost:5000/todo2/todo2').json()")

print('curl http://localhost:5000/todo0 -d "data=Remember the milk" -X PUT')
print('curl http://localhost:5000/todo0')
print('curl http://127.0.0.1:5000/todo1/id1')
print('http://127.0.0.1:5000/todo2/id1')
print('http://127.0.0.1:5000/todo3/id1')

if __name__ == '__main__':
    app.run(debug=True)