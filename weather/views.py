from rest_framework.response import Response
from decouple import config
import requests
from rest_framework.views import APIView
from .serializers import GetWeatherSerializer
from drf_yasg.utils import swagger_auto_schema
import logging   


class GetWeather(APIView):
    
        @swagger_auto_schema(
            query_serializer=GetWeatherSerializer,
            responses={200: GetWeatherSerializer(many=True)}
        )

        def get(self, request):

            API_key = config('API_KEY')
            city = request.GET.get('city')
            
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}&units=metric'
            response = requests.get(url)
            informations = response.json()

            logger = logging.getLogger(__name__)
            logger.warning(informations)

            if response.status_code == 200:
                
                weather = {
                    'city': informations['name'],
                    'tempreature': int(informations['main']['temp']),
                    'description': informations['weather'][0]['description']
                }
                serializer = GetWeatherSerializer(weather, data=weather)
                serializer.is_valid(raise_exception=True)

                return Response(serializer.data)
           
            else:
                logger.error(f"Failed to fetch weather data for {city}. Status code: {response.status_code}")
                return Response({"error": f"Failed to fetch weather data for {city}."}, status=response.status_code)
            
            
    





