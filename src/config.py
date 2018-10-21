import json
import os


if 'SERVERTYPE' in os.environ and os.environ['SERVERTYPE'] == 'AWS Lambda':
    json_data = open('zappa_settings.json')
    env_vars = json.load(json_data)['dev']['environment_variables']
    for key, val in env_vars.items():
        os.environ[key] = val

WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
WEATHER_API_URL = os.environ.get("WEATHER_API_URL")
