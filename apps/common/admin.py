from django.contrib import admin
from .models import User, WeatherData

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname', 'username', 'is_staff', 'is_active')
    search_fields = ('name', 'surname', 'username')

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country', 'lat', 'lon', 'temp_c', 'created_at')
    list_filter = ('name', 'created_at', 'country', 'temp_c')
    search_fields = ('name', 'created_at', 'country', 'temp_c')
