from rest_framework import serializers
from .models import Order


class OrderDeserializer(serializers.ModelSerializer):
    products = serializers.ListField(allow_empty=False)

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def save(self, **kwargs):
        if 'products' in self.validated_data:
            del self.validated_data['products']
        return super().save()

    class Meta:
        model = Order
        fields = [
            'address',
            'firstname',
            'lastname',
            'phonenumber',
            'products',
        ]


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            'id',
            'firstname',
            'lastname',
            'phonenumber',
            'address',
        ]
