from rest_framework import serializers


class GetWeatherSerializer(serializers.Serializer):

    city = serializers.CharField(max_length=100)
    tempreature = serializers.IntegerField()
    description = serializers.CharField(max_length=100)