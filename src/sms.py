from src import dynamodb
from src.weather import fetch_weather, map_weather
from zappa.async import task
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
)


def batch_sms_weather():
    result = dynamodb.scan()

    if result["Count"] == 0:
        return
    rows = result["Items"]
    for row in rows:
        res = fetch_weather(row["city"])
        if res.ok:
            weather_data = map_weather(res.json())
            message = serialize_for_sms(weather_data)
            # but we're really not
            logging.info(f"Sending {row['city']} weather alert to {row['phone_number']}")


def serialize_for_sms(weather):
    """
    Serialize weather details dictionary to SMS appropriate format
    """
    return f"""Here's the weather for {weather['city']}:
    Temperature: {weather["temp"]} C
    Weather: {weather["weather"]["main"]}
    Description: {weather["weather"]["description"]}
    """


if __name__ == "__main__":
    batch_sms_weather()
