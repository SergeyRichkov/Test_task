from rest_framework import serializers, viewsets
from store.models import Sales


class SalesSerializer(serializers.ModelSerializer):
    """Serializer для продаж."""

    class Meta:
        model = Sales
        fields = ('customer', 'item', 'total', 'quantity', 'date')

