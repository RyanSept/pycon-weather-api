from src import api
from src.views import HelloWorld, Weather

api.add_resource(HelloWorld, '/')
api.add_resource(Weather, '/weather')
