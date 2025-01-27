from . import views
from django.urls import include, path

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view(), name='register'),
]