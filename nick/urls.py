from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather, name='weather'),
    path('weather-data/',views.weather_data,name='weather_data'),
    path('add-city/',views.add_city,name='add-city'),
    path('saved-cities/',views.saved_cities,name='saved-cities'),
    path('geo-location/',views.get_geolocation,name='geolocation'),
]