from rest_framework import serializers
from .models import TimeSlot, Doctor

class DoctorSerializer(serializers.ModelSerializer):
     class Meta:
        model = Doctor
        fields = ['doctor_id', 'first_name', 'last_name', 'specialization']

class TimeSlotSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    class Meta:
        model = TimeSlot
        fields = ['id', 'doctor', 'start', 'end', 'is_available']