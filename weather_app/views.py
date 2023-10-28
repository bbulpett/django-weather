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

        current_weather1 = format_current_weather(city1_weather['current'])
        daily_forecasts1 = format_daily_forecast(city1_weather['daily'])

        # TODO: Try to get data for both cities in one request
        if city2:
            # Get coordinates from city 2 name
            lat, lon = fetch_city_coordinates(city2, API_KEY, geocoding_url)
            city2_weather = fetch_weather_data(lat, lon, API_KEY, weather_url)

            current_weather2 = format_current_weather(city2_weather['current'])
            daily_forecasts2 = format_daily_forecast(city2_weather['daily'])
        else:
            current_weather2, daily_forecasts2 = None, None

        # Build the context dictionary to pass to the template
        context = {
            "city1": city1,
            "current_weather1": current_weather1,
            "daily_forecasts1": daily_forecasts1,
            "city2": city2,
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

def format_current_weather(current_weather_data):
    return {
        "temperature": round(current_weather_data['temp'] - 273.15, 2),
        "description": current_weather_data['weather'][0]['description'],
        "icon": current_weather_data['weather'][0]['icon']
    }

def format_daily_forecast(daily_forecast_data):
    forecast_data = []

    for day in daily_forecast_data:
        forecast_data.append(
            {
                "day": datetime.datetime.fromtimestamp(day['dt']).strftime("%A"),
                "min_temp": round(day['temp']['min'] - 273.15, 2),
                "max_temp": round(day['temp']['max'] - 273.15, 2),
                "description": day['weather'][0]['description'],
                "icon": day['weather'][0]['icon']
            }
        )

    return forecast_data
