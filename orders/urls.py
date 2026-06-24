from django.urls import path
from .views import CreateOrder, NewStatus

urlpatterns = [
    path('orders/create/', CreateOrder.as_view(), name='create_order'),
    path('orders/<int:order_id>/status/', NewStatus.as_view(), name='change_order_status')
]