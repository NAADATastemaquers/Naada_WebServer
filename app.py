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
            print("here")
            artists = []
            result = db.naada_artists.find({})
            for artist in result:
                artists.append({
                    "artist": artist['artist'],
                    "artist_img": artist['artist_img'],
                    "artist_desc": artist['artist_desc']
                })
            return artist, 200
        # return selected artist
        result = db.naada_artists.find_one({"_id": ObjectId(id)})
        artist = {
            "artist": result['artist'],
            "artist_img": result['artist_img'],
            "artist_desc": result['artist_desc']
        }
        return artist, 200


api.add_resource(Residents, '/residents', '/residents/<id>')

if __name__ == '__main__':
    app.run(debug=True)
