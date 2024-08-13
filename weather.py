import requests
import os
from dotenv import load_dotenv
load_dotenv()


API_URL = "https://api.openweathermap.org/data/2.5/group"
API_KEY = os.getenv('API_KEY')

def get_weather_data(city_ids):
    params = {
        'id': ','.join(map(str, city_ids)),
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(API_URL, params=params)
    print(response.json())
    return response.json() if response.status_code == 200 else None

