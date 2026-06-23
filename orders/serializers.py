from rest_framework import serializers


class OrderItemSerializer(serializers.Serializer):
    dish_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    modifiers = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        default=[]
    )

class OrderCreateSerializer(serializers.Serializer):
    table_id = serializers.IntegerField()
    items = OrderItemSerializer(many=True)
