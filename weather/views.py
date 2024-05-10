from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from decouple import config
import requests
from rest_framework.views import APIView
from .serializers import GetWeatherSerializer
from drf_yasg.utils import swagger_auto_schema



# @api_view(['GET'])
# def get_weather(request):

#     API_key = config('API_KEY')
#     city = request.GET.get('city')
#     url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}&units=metric'
#     response = requests.get(url)
#     informations = response.json()

#     if response.status_code == 200:
#         return Response({
#             'City' : informations['name'],
#             'Tempreature' : int(informations['main']['temp']),
#             'Description' : informations['weather'][0]['description']
#         }, status = status.HTTP_200_OK)
    
#     else:
#         return Response({
#             'Something is Wrong'
#         })
    

class GetWeather(APIView):

    @swagger_auto_schema(
        request_body=GetWeatherSerializer,
        responses={200: GetWeatherSerializer}
    )

    def post(self, request):

        API_key = config('API_KEY')
        city = request.GET.get('city')
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}&units=metric'
        response = requests.get(url)
        informations = response.json()
        weather = {
            'city' : informations['name'],
            'tempreature' : int(informations['main']['temp']),
            'description' : informations['weather'][0]['description']
        }

        serializer = GetWeatherSerializer(weather)
        return Response(serializer.data)