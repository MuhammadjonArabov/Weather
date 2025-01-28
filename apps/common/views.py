import os
from django.contrib.sites import requests
from django.http import JsonResponse
import requests
from rest_framework.views import APIView
from . import serializers, models, permission
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = serializers.RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "message": "User registered successfully!",
            "user": {
                "id": user.id,
                "username": user.username,
                "name": user.name,
                "surname": user.surname
            }
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response({
            "message": "Login successful!",
            "user": {
                "id": user.id,
                "username": user.username,
                "name": user.name,
                "surname": user.surname
            },
            "tokens": tokens
        }, status=status.HTTP_200_OK)


class WeatherDataAPIView(APIView):
    permission_classes = [permission.IsRegisteredAndLoggedIn]

    def get_weather_data(self, country):
        api_key = os.getenv("WEATHER_API_KEY")
        url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={country}"
        response = requests.get(url)
        return response.json()

    def get(self, request):
        country = request.query_params.get('q', None)
        if not country:
            return JsonResponse({"error": "Country name is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = self.get_weather_data(country)
            temp_color = self.get_temp_color(data['current']['temp_c'])
            wind_color = self.get_wind_color(data['current']['wind_kph'])
            cloud_color = self.get_cloud_color(data['current']['cloud'])

            weather_data = {
                "name": data["location"]["name"],
                "country": data["location"]["country"],
                "lat": data["location"]["lat"],
                "lon": data["location"]["lon"],
                "temp_c": data["current"]["temp_c"],
                "temp_color": temp_color,
                "wind_kph": data["current"]["wind_kph"],
                "wind_color": wind_color,
                "cloud": data["current"]["cloud"],
                "cloud_color": cloud_color
            }

            models.WeatherData.objects.update_or_create(
                name=weather_data["name"],
                country=weather_data["country"],
                defaults=weather_data
            )

            serializer = serializers.WeatherDataSerializer(
                models.WeatherData.objects.get(name=weather_data["name"], country=weather_data["country"]))
            return Response(serializer.data)

        except Exception as e:
            return JsonResponse({"error": f"Failed to fetch weather data: {str(e)}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_temp_color(self, temp_c):
        if temp_c <= -30:
            return "#003366"
        elif temp_c <= -20:
            return "#4A90E2"
        elif temp_c <= -10:
            return "#B3DFFD"
        elif temp_c <= 0:
            return "#E6F7FF"
        elif temp_c <= 10:
            return "#D1F2D3"
        elif temp_c <= 20:
            return "#FFFACD"
        elif temp_c <= 30:
            return "#FFCC80"
        elif temp_c <= 40:
            return "#FF7043"
        else:
            return "#D32F2F"

    def get_wind_color(self, wind_kph):
        if wind_kph <= 10:
            return "#E0F7FA"
        elif wind_kph <= 20:
            return "#B2EBF2"
        elif wind_kph <= 40:
            return "#4DD0E1"
        elif wind_kph <= 60:
            return "#0288D1"
        else:
            return "#01579B"

    def get_cloud_color(self, cloud):
        if cloud <= 10:
            return "#FFF9C4"
        elif cloud <= 30:
            return "#FFF176"
        elif cloud <= 60:
            return "#E0E0E0"
        elif cloud <= 90:
            return "#9E9E9E"
        else:
            return "#616161"
