import pytest
from decimal import Decimal

from accounts.models import CustomUser
from orders.models import Table
from menu.models import Category, Dish

@pytest.fixture
def user(db):
    return CustomUser.objects.create_user(
        username='test_user_123',
        phone_number='+380 11 111 11 11',
        password='test_pass_123',
        role='client',
    )

@pytest.fixture
def table(db):
    return Table.objects.create(
        table_number=1,
        number_of_seats=4,
        status='free',
    )

@pytest.fixture
def category(db):
    return Category.objects.create(
        name='Pizza',
        slug='pizza',   
    )

@pytest.fixture
def dish(db, category):
    return Dish.objects.create(
        name='Margherita',
        description='Classic pizza',
        price=Decimal('200.0'),
        is_active=True,
        preparation_time=20,
        category=category,
    )