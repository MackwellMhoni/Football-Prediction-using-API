import requests
import pytz
import os
from datetime import *

api_timezone = pytz.timezone("Europe/Madrid")
local_timezone = pytz.timezone("Africa/Johannesburg")


def get_current_datetime():
    madrid = datetime.now(tz=timezone.utc).astimezone(api_timezone)
    return madrid

#ensures that certain code only runs when a script is executed directly
def to_local_datetime(start_date):
    local_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
    return api_timezone.localize(local_date).astimezone(local_timezone)


if __name__ == "__main__":
    # this is a datetime object with the timezone used by our api
    current_server_time = get_current_datetime()

    # obtaining the next day as python date object
    tomorrow = current_server_time.date() + timedelta(days=1)

    # setting our API key for auth
    headers = {
        'User-Agent': 'python_requests',
        "X-RapidAPI-Key": "ed42443d22mshc07e63312bfe71bp1684f9jsn5fc616bc8ca9",
    }

    session = requests.Session()
    session.headers = headers

    # setting query params
    params = {
        "iso_date": tomorrow.isoformat(), # python date object should be transformed to ISO format (YYYY-MM-DD)
        "federation": "UEFA",
        "market": "classic"
    }

    prediction_endpoint = "https://football-prediction-api.p.rapidapi.com/api/v2/predictions"
    response = session.get(prediction_endpoint, params=params)
    print(response.json())

#___________________________________________UI___________________________________
