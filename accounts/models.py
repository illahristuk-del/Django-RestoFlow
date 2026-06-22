from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin'
        MANAGER = 'manager'
        COOK = 'cook'
        COURIER = 'courier'

    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=15, choices=Role.choices)
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []