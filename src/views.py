from flask_restful import Resource
from flask_restful import reqparse
from src import app
from src.config import WEATHER_API_URL, WEATHER_API_KEY
import requests


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


parser = reqparse.RequestParser()
parser.add_argument('city', type=str, help='Required query parameter',
                    required=True)


class Weather(Resource):
    def get(self):
        response = {"weather": {}, "ok": True, "message": "Not found."}
        city = parser.parse_args()["city"]

        res = requests.get(f"{WEATHER_API_URL}/weather", params={
            "q": city,
            "units": "metric",
            "APPID": WEATHER_API_KEY
        })
        res_json = res.json()

        if res.status_code not in [200, 404]:
            response.update({
                "ok": False,
                "message": "Something went wrong.",
            })
            app.logger.error(res_json)
            return response, 500

        if "weather" in res_json:
            weather = {
                "id": res_json["id"],
                "name": f"{res_json['name']}, {res_json['sys']['country']}",
                "temp": res_json["main"]["temp"],
                "weather": res_json["weather"][0]
            }
            response["weather"] = weather
            response["message"] = "Success"
        return response
