from flask import Flask
from flask_restful import Resource, Api
from bson.objectid import ObjectId
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient()
client = MongoClient('mongodb+srv://admin:admin@cluster0-ueieq.mongodb.net/test?retryWrites=true&w=majority')
db = client['naada']


class Residents(Resource):
    def get(self, id=None):
        if not id:
            artists = []
            result = db.naada_artists.find()
            for artist in result:
                artists.append({
                    "artist": artist['artist'],
                    "artist_img": artist['artist_img'],
                    "artist_desc": artist['artist_desc']
                })
            return artists, 200
        # return selected artist
        result = db.naada_artists.find_one({"_id": ObjectId(id)})
        artist = {
            "artist": result['artist'],
            "artist_img": result['artist_img'],
            "artist_desc": result['artist_desc'],
            "artist_shows":result['artist_shows']
        }
        return artist, 200

class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        name = data['name']
        result = check_func(data)
        newUser = {
            "username": username,
            "password": password,
            "name": name
        }
        if result != 0:
            objId = db.Users.insert_one(newUser).inserted_id
            id = str(objId)
            return {"id": id}, 201
        else:
            objId = db.Users.find_one({"username": username, "password": password, "name": name})
            id = str(objId["_id"])
            return {"result": "not registered user already present", "id": id}, 201
        
api.add_resource(Residents, '/residents', '/residents/<id>')

if __name__ == '__main__':
    app.run(debug=True)
