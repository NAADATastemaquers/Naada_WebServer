from flask import Flask
from flask_restful import Resource, Api
app = Flask(__name__)
api = Api(app)
class People(Resource):

    def get(self, id=None):
        if not id:
            return {'name': 'John Doe'}
        return [{'name': 'John Doe'}, {'name': 'Mary Canary'}]


api.add_resource(People, '/api/people', '/api/people/<id>')

if __name__ == '__main__':
    app.run(debug=True)