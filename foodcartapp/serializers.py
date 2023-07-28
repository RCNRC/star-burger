from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from .models import Order, Product, OrderItem


class ProductsValidationException(APIException):
    status_code = status.HTTP_200_OK
    default_detail = 'Invalid primary key'


class OrderItemDeserializer(serializers.ModelSerializer):
    product = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def create(self, validated_data):
        product_id = validated_data['product']
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist as exception:
            raise ProductsValidationException(
                detail={
                    'error': f'products: Invalid primary key {product_id}'
                },
            ) from exception
        return OrderItem.objects.create(
            item=product,
            previous_price=product.price,
            count=validated_data['quantity'],
            order=validated_data['order'],
        )

    class Meta:
        model = OrderItem
        fields = (
            'product',
            'quantity',
            'order',
        )


class OrderDeserializer(serializers.ModelSerializer):
    products = serializers.ListField(allow_empty=False)

    def create(self, validated_data):
        products = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        for product in products:
            product['order'] = order.id
            order_item_deserializer = OrderItemDeserializer(data=product)
            order_item_deserializer.is_valid(raise_exception=True)
            order_item_deserializer.save()
        return order

    class Meta:
        model = Order
        fields = (
            'address',
            'firstname',
            'lastname',
            'phonenumber',
            'products',
        )
