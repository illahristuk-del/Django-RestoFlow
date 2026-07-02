from decimal import Decimal

from datetime import timedelta

from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from rest_framework.exceptions import ValidationError

from accounts.models import ClientBonus
from orders.models import Table, OrderItem, Order
from menu.models import Modifier, Dish
from orders.tasks import update_order_eta, send_order_notification


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
        
        order = Order.objects.create(
            total_sum=Decimal('0.00'), 
            table=table_instance,
            user=user
        )

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

def accrue_bonus(order):
    user = order.user
    if user.role != 'client':
        raise ValidationError("user is not a client")

    calculate_bonuses = order.total_sum * Decimal('0.05')

    client_bonus = ClientBonus.objects.create(
        client=user,
        order=order,
        bonuses=calculate_bonuses
    )

    return {'client': user, 'order': order, 'bonuses': calculate_bonuses}    

def update_order_status(order_id, new_status):
    with transaction.atomic():
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise ValidationError("Order not found")

        order.transition(new_status)

        if new_status == 'cooking':
            print(f'Notification for kitchen\n')
            print(f'Order: {order}')
        
        if new_status == 'completed':
            order.table.status = 'free'
            order.table.save()
            print(f'Table {order.table.table_number} is free')
            accrue_bonus(order)

        send_order_notification.delay(order.id)    
        
            
def get_popular_dishes():
    week_ago = timezone.now() - timedelta(days=7)

    popular = (
        OrderItem.objects
        .filter(order__created_at__gte=week_ago)
        .values('dish__name')
        .annotate(total=Sum('quantity'))
        .order_by('-total')[:10]
    )

    return list(popular)