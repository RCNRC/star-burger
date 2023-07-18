from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from .models import Order, Product


class ProductsValidationException(APIException):
    status_code = status.HTTP_200_OK
    default_detail = 'Invalid primary key'



class OrderDeserializer(serializers.ModelSerializer):
    products = serializers.ListField(allow_empty=False)

    def create(self, validated_data):
        return Order.objects.create(**validated_data)

    def save(self, **kwargs):
        try:
            if 'products' in self.validated_data:
                for item in self.validated_data['products']:
                    Product.objects.get(
                        id=item['product']
                    )
                del self.validated_data['products']
        except Product.DoesNotExist as exception:
            raise ProductsValidationException(
                detail={
                    'error': f'products: Invalid primary key {item["product"]}'
                },
            ) from exception
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
