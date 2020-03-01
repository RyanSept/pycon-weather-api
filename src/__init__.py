from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import boto3

app = Flask(__name__)
CORS(app)
api = Api(app)
dynamodb = boto3.resource(
    "dynamodb", region_name="eu-west-2").Table("weather-app-sms-subs")
