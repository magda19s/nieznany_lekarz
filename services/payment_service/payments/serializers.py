from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'visit_id', 'status', 'amount', 'currency', 'created_at', 'updated_at']


class PaymentStatusUpdateSerializer(serializers.Serializer):
    status = serializers.CharField()