import datetime
import requests
from django.shortcuts import render

# Create your views here.
def index(request):
    API_KEY = open("API_KEY", "r").read()
    # URL for the current weather "now"
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?" \
                          "q={}&appid={}"
    # URL for the forecast weather
    forecast_url = "https://api.openweathermap.org/data/2.5/onecall=?" \
                    "lat={}&lon={}&exclude=current,minutely,hourly,alerts" \
                    "&appid={}"

    if request.method == "POST":
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(
                city1, API_KEY, current_weather_url, forecast_url
            )
        
        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(
                city2, API_KEY, current_weather_url, forecast_url
            )
        else:
            weather_data2, daily_forecasts2 = None, None

        # Build the context dictionary to pass to the template
        context = {
            "weather_data1": weather_data1,
            "daily_forecasts1": daily_forecasts1,
            "weather_data2": weather_data2,
            "daily_forecasts2": daily_forecasts2
        }

        return(request, "weather_app/index.html", context)
    else:
        return render(request, "weather_app/index.html")

# Send a request to the OpenWeatherMap API and render data into template
def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    # Get response as a JSON object so it can be treated like a dictionary
    response = requests.get(current_weather_url.format(city, api_key)).json()

    print("*******************************************************************")
    print(current_weather_url.format(city, api_key))
    print(response)
    print("*******************************************************************")

    # import code; code.interact(local=dict(globals(), **locals()))

    # Extract coordinates from response
    lat, lon = response['coord']['lat'], response['coord']['lon']

    # Use coordinates to get weather data from forecase url
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

    # Extract data from current weather response, formatted for the template
    weather_data = {
        "city": city,
        "temperature": round(response['main']['temp'] - 273.15, 2),  # Convert from Kelvin to Celsius
        "description": response['weather'][0]['description'],
        "icon": response['weather'][0]['icon']
    }

    # Extract data from forecast response, formatted for the template
    daily_forecasts = []

    for daily_data in forecast_response['daily'][:5]:
        daily_forecasts.append(
            {
                "day": datetime.datetime.fromtimestamp(daily_data['dt']).strftime("%A"),
                "min_temp": round(daily_data['temp']['min'] - 273.15, 2),
                "max_temp": round(daily_data['temp']['max'] - 273.15, 2),
                "description": daily_data['weather'][0]['description'],
                "icon": daily_data['weather'][0]['icon']
            }
        )

    return weather_data, daily_forecasts
