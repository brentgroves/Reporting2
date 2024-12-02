# https://blog.devgenius.io/how-to-deploy-rest-api-application-using-mysql-on-the-kubernetes-cluster-4c806de1a48
# https://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api
# https://ch-rowley.github.io/2021/10/24/How-to-marshal-data-with-Flask.html
# https://marshmallow.readthedocs.io/en/stable/marshmallow.fields.html
from flask import Flask, request
from flask_restful import Api, Resource, abort, reqparse
from marshmallow import Schema, ValidationError, fields

app = Flask(__name__)
api = Api(app)

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
    # curl http://localhost:5000/hotel
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
    def put(self, hotel_id):
        hotels[hotel_id] = request.form['data']
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


if __name__ == '__main__':
    # app.run(debug=True)
    # app.run(host='0.0.0.0', port=int(FLASK_APP_PORT))    
    app.run(host='0.0.0.0', port=5000)    
