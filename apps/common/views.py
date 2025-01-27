from django.shortcuts import render
from . import serializers
from rest_framework import generics

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = serializers.RegisterSerializer
