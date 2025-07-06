from django.shortcuts import render, redirect,get_object_or_404
import requests
from .models import City
from django.http import JsonResponse
from .forms import CityForm


def weather(request):
    cities=City.objects.all()
    if request.method == 'POST':
        request.session['post_data']=request.POST.dict()
        return redirect(weather_data)


    return render(request, 'nick/weather.html', {})


def weather_data(request):


    WEATHER_THEMES = {
        "Clear": "sunny-theme",
        "Clouds": "cloudy-theme",
        "overcast-clouds": "cloudy-theme",
        "Rain": "rainy-theme",
        "Snow": "snowy-theme",
        "Thunderstorm": "stormy-theme",
        "Mist": "misty-theme",
        "Haze": "misty-theme",
        "Drizzle": "rainy-theme",
    }

    error_message = None
    weather_data = None
    theme = "default-theme"

    data = request.session.get('post_data')
    city = data.get('city') if data else None

    if city:
        api_key = 'd8521259681afe849ad85a25b0a2e151'
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'

        response = requests.get(url)

        if response.status_code == 200:
            # Parse the response if it's successful
            weather_data = response.json()

            # Determine the theme based on the weather condition
            weather_condition = weather_data["weather"][0]["main"]
            theme = WEATHER_THEMES.get(weather_condition, "default-theme")
        else:
            error_message = 'City not found. Please try again.'
    else:
        error_message = 'No city provided. Please enter a city name.'

    return render(request, 'nick/data.html', {
        'weather_data': weather_data,
        'error_message': error_message,
        'theme': theme,  # Pass the theme to the template
    })



def add_city(request):
    error_message = None
    weather_data = None

    if request.method == 'POST':
        city = request.POST.get('city')

        if city:
            # Fetch data from the API using the entered city
            api_key = 'd8521259681afe849ad85a25b0a2e151'  # Replace with your actual OpenWeatherMap API key
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
            
            # Make the API request
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                # Check if the city is already saved
                if not City.objects.filter(name=city).exists():
                    weather_data = {
                        'temperature': data['main']['temp'],
                        'city': city,
                        'description': data['weather'][0]['description']
                    }

                    # Save the city and temperature to the database
                    City.objects.create(name=city, temperature=weather_data['temperature'])
                else:
                    error_message = f"The city '{city}' is already saved."
            else:
                error_message = 'City not found or invalid input!'

            return redirect(saved_cities)  # Redirect to saved_cities after adding a city

    return render(request, 'nick/add_city.html', {'error_message': error_message, 'weather_data': weather_data})


def saved_cities(request):
    api_key = 'd8521259681afe849ad85a25b0a2e151'  # Replace with your actual OpenWeatherMap API key
    cities = City.objects.all()  # Retrieve all saved cities from the database
    weather_data = []

    for city in cities:
        # Fetch updated weather data for each city
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city.name}&appid={api_key}&units=metric'
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            # Update the city's temperature in the database
            city.temperature = data['main']['temp']
            city.save()

            # Append real-time data to the weather_data list
            weather_data.append({
                'city': city.name,
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description']
            })
        else:
            # Handle API errors (optional)
            weather_data.append({
                'city': city.name,
                'temperature': 'N/A',
                'description': 'Error fetching data'
            })  
    return render(request, 'nick/saved_city.html', {'weather_data': weather_data})


def get_geolocation(request):
    return render(request,'nick/geolocation.html')
