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
    amount = serializers.FloatField()

class TimeSlotSerializer(serializers.Serializer):
    id = serializers.CharField()
    doctor = DoctorDataSerializer()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    is_available = serializers.BooleanField()

class VisitPayloadSerializer(serializers.Serializer):
    id = serializers.CharField()
    doctor = DoctorDataSerializer()
    patient_id = serializers.CharField()
    time_slot = TimeSlotSerializer()
    status = serializers.CharField()
    notes = serializers.CharField(allow_blank=True, allow_null=True, required=False)