from flask import Flask
from flask_restful import Resource, Api, request
from bson.objectid import ObjectId
from pymongo import MongoClient
from datetime import datetime

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
                    "artist_desc": artist['artist_desc'],
                    "artist_id": str(artist['_id'])
                })
            return artists, 200
        # return selected artist
        result = db.naada_artists.find_one({"_id": ObjectId(id)})
        artist = {
            "artist": result['artist'],
            "artist_img": result['artist_img'],
            "artist_desc": result['artist_desc'],
            "artist_shows": result['artist_shows']
        }
        return artist, 200


class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        email = data['email']
        result = check_func(data)
        newUser = {
            "username": username,
            "password": password,
            "email": email
        }
        if result != 0:
            objId = db.naada_users.insert_one(newUser).inserted_id
            id = str(objId)
            return {"id": id}, 201
        else:
            objId = db.naada_users.find_one({"username": username, "password": password, "email": email})
            id = str(objId["_id"])
            return {"result": "not registered user already present", "id": id}, 201


def check_func(data):
    results = db.naada_users.find({"username": data['username'], "email": data['email'], "password": data['password']})
    if results.count() is 0:
        return 1
    for result in results:
        return 0


class UserDetails(Resource):
    def get(self, userID):
        user = db.naada_users.find_one({"_id": ObjectId(userID)})
        username = user['username']
        email = user['email']
        return {"username": username, "email": email}, 200

    def post(self):
        data = request.get_json();
        newResident = {
            "artist": data["artist"],
            "artist_img": data["artist_img"],
            "artist_desc": data["artist_desc"],
            "artist_shows": data["artist_shows"]
        }
        objId = db.naada_artists.insert_one(newResident)
        return {"success": "created new resident"}, 200


class Message(Resource):
    def get(self, index):
        if int(index) != 0:
            all_messages = db.naada_message.find().limit(int(index))
            toSend = []
            for message in all_messages:
                toSend.append({
                    'message': message['message'],
                    'sender': message['sender'],
                    'timestamp': str(message['timestamp'])
                })
            return toSend, 200
        else:
            all_messages = db.naada_message.find()
            toSend = []
            for message in all_messages:
                if message['timestamp'] is None:
                    date = 'no timestamp'
                else:
                    date = message['timestamp']
                toSend.append({
                    'message': message['message'],
                    'sender': message['sender'],
                    'timestamp': str(date)
                })
            return toSend, 200

    def post(self, index):
        data = request.get_json()
        newMessage = {
            "message": data["message"],
            "sender": data["sender"],
            "timestamp": datetime.now()
        }
        objId = db.naada_message.insert_one(newMessage)
        return {"success": "added new message"}, 200


class Favorite(Resource):
    def get(self, userID):
        if userID is not str(0):
            all_fav = []
            data = db.user_fav.find({"_id": ObjectId(userID)})
            for dat in data:
                all_fav.append({
                    "userID": data["userID"],
                    "song_name": data["song_name"],
                    "song_url": data["song_url"],
                    "song_img": data["song_img"]
                })
        return all_fav,200

    def post(self):
        data = request.get_json()
        fav_data ={
            "userID": data["userID"],
            "song_name": data["song_name"],
            "song_url": data["song_url"],
            "song_img": data["song_img"]
        }
        objId = db.user_fav.insert_one(fav_data)
        return {"success": "added new favorite song"}, 200




api.add_resource(Residents, '/residents', '/residents/<id>')
api.add_resource(Register, '/register')
api.add_resource(UserDetails, '/userdetails/<string:userID>')
api.add_resource(Message, '/message/<string:index>')

if __name__ == '__main__':
    app.run(debug=True)
