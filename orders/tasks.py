from celery import shared_task
from django.utils import timezone
from datetime import timedelta 


@shared_task
def update_order_eta(order_id):
    from .models import Order

    total_minutes  = 0

    order = Order.objects.get(id=order_id)
    
    for item in order.items.all():
        total_minutes += item.dish.preparation_time

    order.eta = timezone.now() + timedelta(minutes=total_minutes)
    order.save()
 