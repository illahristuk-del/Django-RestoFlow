import pytest
from decimal import Decimal
from django.test import override_settings
from orders.models import Order
from orders.services import accrue_bonus, create_order


@pytest.mark.django_db
def test_accrue_bonus(user, table):
    order = Order.objects.create(
        total_sum=Decimal("500.0"),
        table=table,
        user=user,
    )

    result = accrue_bonus(order)

    assert result["bonuses"] == Decimal("25.00")


@pytest.mark.django_db
def test_valid_transition(user, table):
    order = Order.objects.create(
        total_sum=Decimal("150.0"),
        table=table,
        user=user,
    )

    order.transition("cooking")

    assert order.status == "cooking"


@pytest.mark.django_db
def test_invalid_transition(user, table):
    order = Order.objects.create(
        total_sum=Decimal("350.0"),
        table=table,
        user=user,
    )

    with pytest.raises(ValueError):
        order.transition("completed")


@pytest.mark.django_db
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
def test_create_order_sum(user, table, dish):
    items = [{"dish_id": dish.id, "quantity": 2, "modifiers": []}]

    order = create_order(user, table.id, items)

    assert order.total_sum == Decimal("400.00")
