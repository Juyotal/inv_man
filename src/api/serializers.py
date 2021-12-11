from rest_framework import serializers
from .models import Item, Store


class ItemSerializer(serializers.ModelSerializer):
    profit = serializers.ReadOnlyField()
    class Meta:
        model = Item
        fields = '__all__'
 


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
