from decimal import Decimal

from django.db import transaction
from rest_framework.exceptions import ValidationError

from orders.models import Table, OrderItem, Order
from menu.models import Modifier, Dish
from orders.tasks import update_order_eta


def create_order(user, table_id: int, items: list):
    with transaction.atomic():
        try:
            table_instance = Table.objects.select_for_update().get(id=table_id)
        except Table.DoesNotExist:
            raise ValidationError("Table not found")
        
        if not table_instance.status == 'free':
            raise ValidationError("Table is already occupied")
        
        table_instance.status = 'occupied'
        table_instance.save()
        
        order = Order.objects.create(total_sum=Decimal('0.00'), table=table_instance)

        total_sum = Decimal('0.00')

        for item in items:
            try:
                dish = Dish.objects.get(id=item['dish_id'])
            except Dish.DoesNotExist:
                raise ValidationError("Dish not found")
            if not dish.is_active:
                raise ValidationError("Dish is not avaliable")
            quantity = item['quantity']
            modifiers = Modifier.objects.filter(id__in=item['modifiers'])
            modifiers_price = sum((m.price for m in modifiers), Decimal('0.00'))
            item_price = (dish.price + modifiers_price) * quantity

            total_sum += item_price

            order_item = OrderItem.objects.create(
                order=order,
                dish=dish,
                quantity=quantity,
                saved_price=dish.price
            )

            order_item.modifiers.set(modifiers)

        order.total_sum = total_sum
        order.save()
        
        update_order_eta.delay(order.id)

        return order

        