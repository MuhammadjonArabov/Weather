from . import views
from django.urls import include, path

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('weather/', views.WeatherDataAPIView.as_view(), name='weather_data'),
]