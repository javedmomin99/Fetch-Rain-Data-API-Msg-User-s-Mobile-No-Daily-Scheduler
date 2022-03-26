import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
API_key = "645271b12364e08402702c778e6378f9"
account_sid = "ACad5b73164c2c28604236773cfaf1e08c"
auth_token = "edd57271f2e0c8f77a6cc9c3c7f3c97f"

weather_params = {
    "lat": 19.148560,
    "lon": 72.995270,
    "appid": API_key,
    "exclude": "current,minutely,daily",
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_slice = response.json()["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
            body="It's going to Rain Today. Remember to bring an ☂️",
            # from_ = "Trial / Dummy Number Generated"
            from_='+19036229821',
            #to = "User's Number"
            to='+91 72085 07051'
        )
    print(message.status)
    #print(message.body) -> This also Works
#print(weather_data["hourly"][0]["weather"][0]["id"])
#Scheduler : https://www.pythonanywhere.com/user/javedmomin99/files/home/javedmomin99