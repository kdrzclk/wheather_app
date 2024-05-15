from django.urls import path
from .views import GetWeather

urlpatterns = [
     path('weather/', GetWeather.as_view(), name='get_weather'),
    
]





