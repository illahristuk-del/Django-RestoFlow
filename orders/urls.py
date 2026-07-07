from django.urls import path
from .views import CreateOrder, NewStatus, PopularDishes, OrderListFilter

urlpatterns = [
    path("orders/create/", CreateOrder.as_view(), name="create_order"),
    path(
        "orders/<int:order_id>/status/", NewStatus.as_view(), name="change_order_status"
    ),
    path(
        "reports/popular-dishes/",
        PopularDishes.as_view(),
        name="get_top10_popular_dishes",
    ),
    path("orders/", OrderListFilter.as_view(), name="filter_orders_by_date"),
]
