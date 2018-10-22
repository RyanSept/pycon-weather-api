from src import dynamodb, sns
from src.weather import fetch_weather, map_weather
from zappa.async import task
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
)

topic = sns.create_topic(Name="hourly-weather-updates")
topic_arn = topic['TopicArn']


def batch_sms_weather():
    result = dynamodb.scan()
    logging.info(result)
    if result["Count"] == 0:
        return
    cities = result["Items"]
    for city in cities:
        res = fetch_weather(city["city"])
        if res.ok:
            weather_data = map_weather(res.json())
            message = serialize_for_sms(weather_data)
            sns_call = sns.publish(TopicArn=topic_arn, Message=message,
                                   MessageAttributes={
                                       "city": {"DataType": "String",
                                                "StringValue": city["city"]}})
            logging.debug("SNS Response:", sns_call)


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
