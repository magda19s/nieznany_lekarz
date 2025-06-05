from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'visit_id', 'status', 'amount', 'currency', 'created_at', 'updated_at']


class PaymentStatusUpdateSerializer(serializers.Serializer):
    status = serializers.CharField()
    
    
class CreateCheckoutSerializer(serializers.Serializer):
    timeslot_id = serializers.CharField()
    
    
class DoctorDataSerializer(serializers.Serializer):
    doctor_id = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    specialization = serializers.CharField()
    amount = serializers.CharField()

class TimeSlotPayloadSerializer(serializers.Serializer):
    id = serializers.CharField()
    start = serializers.CharField()
    end = serializers.CharField()
    is_available = serializers.BooleanField()
    doctor = DoctorDataSerializer()
