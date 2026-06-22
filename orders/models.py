import uuid
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Table(models.Model):
    class Status(models.TextChoices):
        FREE = 'free', 'Free'
        OCCUPIED = 'occupied', 'Occupied'

    table_number = models.IntegerField(unique=True)
    number_of_seats = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.FREE)

    def __str__(self):
        return f'Table {self.table_number}'


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COOKING = 'cooking', 'Cooking'
        READY = 'ready', 'Ready'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    order_number = models.CharField(max_length=20, unique=True, default=uuid.uuid4, editable=False)
    total_sum = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
    )
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name='orders',
    )

    def __str__(self):
        return f'Order {self.order_number}'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
    )
    dish = models.ForeignKey(
        'menu.Dish',
        on_delete=models.CASCADE,
        related_name='order_items',
    )
    quantity = models.PositiveIntegerField()
    saved_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    modifiers = models.ManyToManyField(
        'menu.Modifier',
        blank=True,
        related_name='order_items',
    )

    def __str__(self):
        return f'{self.dish} x{self.quantity}'