from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User, WeatherData
from django.utils.translation import gettext_lazy as _


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['name', 'surname', 'username', 'password']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(f"This username '{value}' is already taken, please choose another one.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, **validated_data)
        user.is_staff=True
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({'msg': _("User not found")})

        if not user.check_password(password):
            raise serializers.ValidationError({'msg': _("The password is incorrect")})

        attrs['user'] = user
        return attrs


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = ['name', 'country', 'lat', 'lon', 'temp_c', 'temp_color', 'wind_kph', 'wind_color', 'cloud',
                  'cloud_color', 'created_at']
