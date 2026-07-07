from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required")
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")
        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        MANAGER = "manager", "Manager"
        COOK = "cook", "Cook"
        COURIER = "courier", "Courier"
        CLIENT = "client", "Client"

    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=15, choices=Role.choices, default=Role.CLIENT)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class ClientBonus(models.Model):
    client = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="bonuses"
    )

    order = models.ForeignKey(
        "orders.Order", on_delete=models.CASCADE, related_name="order_bonuses"
    )

    bonuses = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client} - {self.bonuses}"
