from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import OrderCreateSerializer, NewStatusSerializer
from .services import create_order, update_order_status, get_popular_dishes

class CreateOrder(APIView):
    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        table_id = serializer.validated_data['table_id']
        items = serializer.validated_data['items']

        order = create_order(request.user, table_id, items)

        return Response(
            {'order_number': str(order.order_number)},
            status=status.HTTP_201_CREATED
            )
    
class NewStatus(APIView):
    def patch(self, request, order_id):
        serializer = NewStatusSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data['status']

        update_status = update_order_status(order_id, new_status)

        return Response(
            {'order_id': order_id, 'order_status': new_status},
            status=status.HTTP_200_OK
        )

@method_decorator(cache_page(60 * 60), name='get')
class PopularDishes(APIView):
    def get(self, request):
        popular_dishes_list = get_popular_dishes()
        return Response(popular_dishes_list)
    
