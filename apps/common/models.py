from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission, Group
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(username, password, **extra_fields)


class User(AbstractUser):
    name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    email = None
    objects = UserManager()

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.username} ({self.name} {self.surname})"


class WeatherData(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    lat = models.FloatField()
    lon = models.FloatField()
    temp_c = models.FloatField()
    temp_color = models.CharField(max_length=10)
    wind_kph = models.FloatField()
    wind_color = models.CharField(max_length=10)
    cloud = models.IntegerField()
    cloud_color = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, {self.country} - {self.temp_c}°C"
