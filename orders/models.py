import uuid
from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator


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

    ALLOWED_TRANSITIONS = {
        'pending': ['cooking', 'cancelled'],
        'cooking': ['ready', 'cancelled'],
        'ready': ['completed', 'cancelled'],
        'completed': [],
        'cancelled': [],
    }


    order_number = models.CharField(max_length=20, unique=True, default=uuid.uuid4, editable=False)
    total_sum = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
    )
    eta = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name='orders',
    )
    user = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='user_orders'
        )

    def __str__(self):
        return f'Order {self.order_number}'

    def transition(self, new_status):
        if new_status not in self.ALLOWED_TRANSITIONS[self.status]:
            raise ValueError(f"Cannot transition from {self.status} to {new_status}")
        self.status = new_status
        self.save()


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
    

class Report(models.Model):
    date = models.DateField(unique=True)
    revenue = models.DecimalField(max_digits=12, decimal_places=2)
    popular_items = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Report {self.date}'
    
