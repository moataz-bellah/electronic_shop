from rest_framework import serializers
from .models import Order,OrderItem,Product
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields=['user','product','quantity','comment']
        #read_only=True
class OrderSerializer(serializers.ModelSerializer):
    #items = serializers.PrimaryKeyRelatedField(queryset=OrderItem.objects.all(),many=True,
    # read_only=False)
    items=OrderItemSerializer(many=True)
    class Meta:
        model=Order
        fields = ['id','user','total_price','paid', 'items']

    def create(self, validated_data,*args, **kwargs):
        tracks_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for track_data in tracks_data:
            OrderItem.objects.create(orders=order, **track_data)
        return order
    """
    def create(self,validated_data):
        orders=validated_data.pop('orders')
        order=Order.objects.create(**validated_data)
        for o in orders:
            OrderItem.objects.create(**o,product=order)
        return order
    """
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
