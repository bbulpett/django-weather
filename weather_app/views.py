from django.shortcuts import render
import requests
import datetime

# Create your views here.
def index(request):
    API_KEY = open("API_KEY", "r").read()

    # Geocoding URL for getting coordinates from city name
    geocoding_url = "https://api.openweathermap.org/geo/1.0/direct?" \
                    "q={}&limit=1&appid={}"
    # URL for the current weather "now"
    weather_url = "https://api.openweathermap.org/data/3.0/onecall?" \
                  "lat={}&lon={}&exclude={}&appid={}"

    if request.method == "POST":
        city1 = request.POST['city1']
        city2 = request.POST['city2'] if request.POST['city2'] else None

        # Get coordinates from city 1 name
        lat, lon = fetch_city_coordinates(city1, API_KEY, geocoding_url)
        city1_weather = fetch_weather_data(lat, lon, API_KEY, weather_url)

        current_weather1 = city1_weather['current']
        daily_forecasts1 = city1_weather['daily']

        # TODO: Try to get data for both cities in one request
        if city2:
            # Get coordinates from city 2 name
            lat, lon = fetch_city_coordinates(city2, API_KEY, geocoding_url)
            city2_weather = fetch_weather_data(lat, lon, API_KEY, weather_url)

            current_weather2 = city2_weather['current']
            daily_forecasts2 = city2_weather['daily']
        else:
            current_weather2, daily_forecasts2 = None, None

        # Build the context dictionary to pass to the template
        context = {
            "current_weather1": current_weather1,
            "daily_forecasts1": daily_forecasts1,
            "current_weather2": current_weather2,
            "daily_forecasts2": daily_forecasts2
        }

        return render(request, "weather_app/index.html", context)
    else:
        return render(request, "weather_app/index.html")


def fetch_city_coordinates(city, api_key, url):
    response = requests.get(url.format(city, api_key)).json()[0]

    return response['lat'], response['lon']


# Send a request to the OpenWeatherMap API and render data into template
def fetch_weather_data(lat, lon, api_key, url):
    EXCLUDES = "minutely,hourly,alerts"

    response = requests.get(url.format(lat, lon, EXCLUDES, api_key)).json()

    return response

# def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):

#     # Get response as a JSON object so it can be treated like a dictionary
#     response = requests.get(current_weather_url.format(city, api_key)).json()

#     # import code; code.interact(local=dict(globals(), **locals()))

#     # Extract coordinates from response
#     lat, lon = response['lat'], response['lon']

#     # Use coordinates to get weather data from forecase url
#     forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

#     # Extract data from current weather response, formatted for the template
#     weather_data = {
#         "city": city,
#         "temperature": round(response['main']['temp'] - 273.15, 2),  # Convert from Kelvin to Celsius
#         "description": response['weather'][0]['description'],
#         "icon": response['weather'][0]['icon']
#     }

#     # Extract data from forecast response, formatted for the template
#     daily_forecasts = []

#     for daily_data in forecast_response['daily'][:5]:
#         daily_forecasts.append(
#             {
#                 "day": datetime.datetime.fromtimestamp(daily_data['dt']).strftime("%A"),
#                 "min_temp": round(daily_data['temp']['min'] - 273.15, 2),
#                 "max_temp": round(daily_data['temp']['max'] - 273.15, 2),
#                 "description": daily_data['weather'][0]['description'],
#                 "icon": daily_data['weather'][0]['icon']
#             }
#         )

#     return weather_data, daily_forecasts
