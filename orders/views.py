from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderCreateSerializer
from .services import create_order

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