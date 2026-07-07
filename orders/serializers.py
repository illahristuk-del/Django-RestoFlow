from rest_framework import serializers
from .models import Order


class OrderItemSerializer(serializers.Serializer):
    dish_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    modifiers = serializers.ListField(
        child=serializers.IntegerField(), required=False, default=[]
    )


class OrderCreateSerializer(serializers.Serializer):
    table_id = serializers.IntegerField()
    items = OrderItemSerializer(many=True)


class NewStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.Status.choices)


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "status",
            "total_sum",
            "eta",
            "created_at",
            "table",
            "user",
        ]
