from flask import Blueprint
from flask_restful import Resource, Api


app = Blueprint('main', __name__)
api = Api(app)

class SimpleAPI(Resource):

    def get(self):
        return {'hello': 'world'}

api.add_resource(SimpleAPI, '/')
