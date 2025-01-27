from rest_framework import serializers
from .models import User, WeatherData


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['name', 'surname', 'username', 'password']

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(f"This username '{value}' is already taken, please choose another one.")
        return value
