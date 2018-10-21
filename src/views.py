from flask_restful import Resource
from flask_restful import reqparse
from src import app, sns, dynamodb
from src.weather import fetch_weather, map_weather
import json


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


class Weather(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('city', type=str, help='Required query parameter',
                            required=True)

        response = {"data": {}, "ok": True, "message": "Not found."}
        city = parser.parse_args()["city"]

        res = fetch_weather(city)
        res_json = res.json()

        if res.status_code not in [200, 404]:
            response.update({
                "ok": False,
                "message": "Something went wrong.",
            })
            app.logger.error(res_json)
            return response, 500

        if "weather" in res_json:
            weather = map_weather(res_json)
            response["data"] = weather
            response["message"] = "Success"
        return response


class Subscribe(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phone_number', type=str, help='Required query parameter',
                            required=True, location="json")
        parser.add_argument('city', type=str, help='Required query parameter',
                            required=True, location="json")
        args = parser.parse_args()

        topic = sns.create_topic(Name="hourly-weather-updates")
        topic_arn = topic['TopicArn']
        subscription_arn = sns.subscribe(TopicArn=topic_arn, Protocol="sms",
                                         Endpoint=args["phone_number"])['SubscriptionArn']

        sns.set_subscription_attributes(
            SubscriptionArn=subscription_arn,
            AttributeName='FilterPolicy',
            AttributeValue=json.dumps({"city": [args["city"]]})
        )
        dynamodb.put_item(Item={"city": args["city"]})

        # send message as a test run
        sns.publish(PhoneNumber=args["phone_number"],
                    Message=f"You've successfully subscribed to weather updates for {args['city']}.")
        return "Ok"
