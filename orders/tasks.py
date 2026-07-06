from celery import shared_task
from django.utils import timezone
from datetime import timedelta 
import time


@shared_task
def update_order_eta(order_id):
    from .models import Order

    total_minutes  = 0

    order = Order.objects.get(id=order_id)
    
    for item in order.items.all():
        total_minutes += item.dish.preparation_time

    order.eta = timezone.now() + timedelta(minutes=total_minutes)
    order.save()
 
@shared_task
def send_order_notification(order_id):
    from .models import Order

    order = Order.objects.get(id=order_id)

    time.sleep(5)

    print(f'notification sent to {order.user.phone_number}\n'
        f'order status updated to -> {order.status}')
    
@shared_task
def generate_monthly_report():
    from orders.models import Order, OrderItem, Report
    from django.db.models import Sum
    from decimal import Decimal

    yesterday = timezone.now().date() - timedelta(days=1)

    revenue = Order.objects.filter(
        created_at__date = yesterday,
        status = 'completed',
    ).aggregate(total=Sum('total_sum'))['total'] or Decimal('0.00')

    popular = list(
        OrderItem.objects
        .filter(order__created_at__date=yesterday)
        .values('dish__name')
        .annotate(total=Sum('quantity'))
        .order_by('-total')[:10]
    )

    Report.objects.create(
        date=yesterday,
        revenue=revenue,
        popular_dishes=popular
    )