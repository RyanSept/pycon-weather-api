from src import api
from src.views import HelloWorld, Weather, Subscribe

api.add_resource(HelloWorld, '/')
api.add_resource(Weather, '/weather')
api.add_resource(Subscribe, '/subscribe')
