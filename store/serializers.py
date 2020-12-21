from rest_framework import serializers, viewsets
from store.models import Sales


class DualSerializerViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.SalesSerializer
        if self.action == 'list':
            return serializers.DettaglioGruppi





class SalesSerializer(serializers.ModelSerializer):
    """Serializer для клиентов."""

    class Meta:
        model = Sales
        fields = ('customer', 'item', 'total', 'quantity', 'date')

