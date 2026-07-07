from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter

from .serializers import OrderCreateSerializer, NewStatusSerializer, OrderSerializer
from .services import create_order, update_order_status, get_popular_dishes
from .filters import OrderFilter
from .models import Order


class CreateOrder(APIView):
    @extend_schema(request=OrderCreateSerializer)
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        table_id = serializer.validated_data["table_id"]
        items = serializer.validated_data["items"]

        order = create_order(request.user, table_id, items)

        return Response(
            {"order_number": str(order.order_number)}, status=status.HTTP_201_CREATED
        )


class NewStatus(APIView):
    @extend_schema(request=NewStatusSerializer)
    def patch(self, request, order_id):
        serializer = NewStatusSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data["status"]

        update_status = update_order_status(order_id, new_status)

        return Response(
            {"order_id": order_id, "order_status": new_status},
            status=status.HTTP_200_OK,
        )


class OrderListFilter(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = OrderFilter
    search_fields = ["order_number"]


@method_decorator(cache_page(60 * 60), name="get")
class PopularDishes(APIView):
    def get(self, request):
        popular_dishes_list = get_popular_dishes()
        return Response(popular_dishes_list)
