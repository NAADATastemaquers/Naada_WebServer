from flask import Flask
from flask_restful import Resource, Api
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient()
client = MongoClient('mongodb+srv://admin:admin@cluster0-ueieq.mongodb.net/test?retryWrites=true&w=majority')

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
