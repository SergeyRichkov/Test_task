from abc import ABC

from rest_framework import serializers, viewsets
from store.models import Sales


class SalesSerializer(serializers.ModelSerializer):
    """Serializer для продаж."""

    class Meta:
        model = Sales
        fields = ('customer', 'item', 'total', 'quantity', 'date')


class CustomerSerializer(serializers.Serializer):
    spent_money = serializers.FloatField()
    username = serializers.CharField()
    gems = serializers.ListField()


class CustomersSerializer(serializers.Serializer):
    response = serializers.ListField(child=CustomerSerializer())


class DualSerializerViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'create':
            return SalesSerializer
        if self.action == 'list':
            return CustomersSerializer
