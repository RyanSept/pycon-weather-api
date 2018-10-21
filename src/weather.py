from src.config import WEATHER_API_URL, WEATHER_API_KEY
import requests


def fetch_weather(city):
    """
    Fetch weather for given city
    :param city: str
    :returns dict: OpenWeatherMapAPI weather response for city
    """
    res = requests.get(f"{WEATHER_API_URL}/weather", params={
        "q": city,
        "units": "metric",
        "APPID": WEATHER_API_KEY
    })
    return res


def map_weather(response):
    """
    Map OpenWeatherMap API response to format we want
    :param response: dict object
    """
    return {
        "id": response["id"],
        "city": f"{response['name']}, {response['sys']['country']}",
        "temp": response["main"]["temp"],
        "weather": response["weather"][0]
    }
