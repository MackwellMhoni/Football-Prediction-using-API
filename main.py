import requests
import pytz
import os
from datetime import *

#Calling the football prediction API
API_KEY = "https://football-prediction-api.p.rapidapi.com/api/v2/list-markets"

api_timezone = pytz.timezone("Europe/Madrid")
local_timezone = pytz.timezone("Africa/Johannesburg")

response = requests.get(API_KEY)

def get_current_datetime():
    madrid = datetime.now(tz=timezone.utc).astimezone(api_timezone)
    return madrid

print(get_current_datetime())
#___________________________________________UI____________________________________________
