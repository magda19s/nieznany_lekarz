from rest_framework import serializers
from .models import TimeSlot, Doctor, Visit

class DoctorSerializer(serializers.ModelSerializer):
     class Meta:
        model = Doctor
        fields = ['doctor_id', 'first_name', 'last_name', 'specialization']

class TimeSlotSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    class Meta:
        model = TimeSlot
        fields = ['id', 'doctor', 'start', 'end', 'is_available']

class VisitCreateSerializer(serializers.Serializer):
    time_slot_id = serializers.CharField()
    patient_id = serializers.CharField()

class VisitSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    time_slot  = TimeSlotSerializer()
    class Meta:
        model = Visit
        fields = ['id', 'doctor', 'patient_id', 'time_slot', 'status', 'notes', 'variant']

class VisitNotesUpdateSerializer(serializers.Serializer):
    notes = serializers.CharField()
class VisitStatusUpdateSerializer(serializers.Serializer):
    status = serializers.CharField()