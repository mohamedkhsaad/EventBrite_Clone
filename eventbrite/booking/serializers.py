from rest_framework import serializers
from booking.models import *


class TicketClassSerializer(serializers.ModelSerializer):

    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = TicketClass
        exclude = ['id']


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('ticket_class_id', 'quantity','order_id','ticket_price')

    # def create(self, validated_data):
    #     ticket_class = validated_data.get('ticket_class')
    #     quantity = validated_data.get('quantity')
    #     order = validated_data.get('order')
    #     ticket_price = ticket_class.price if ticket_class and isinstance(ticket_class, TicketClass) else None
    #     order_item = OrderItem.objects.create(ticket_class=ticket_class,
    #                                             quantity=quantity,
    #                                            order=order,
    #                                            ticket_price=ticket_price)
    #     return order_item
    
    # def get_ticket_class(self,obj):
    #     ticket_class_data = obj.ticket_class
    #     print(ticket_class_data)
    #     print("===========")
    #     if isinstance(ticket_class_data, TicketClass):
    #         return ticket_class_data
    #     elif isinstance(ticket_class_data, int):
    #         try:
    #             return TicketClass.objects.get(pk=ticket_class_data)
    #         except TicketClass.DoesNotExist:
    #             raise serializers.ValidationError('Invalid ticket class')
    #     else:
    #         raise serializers.ValidationError('Invalid ticket class')

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('user_id')

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for order_item_data in order_items_data:
            OrderItem.objects.create(order=order, **order_item_data)
        return order

