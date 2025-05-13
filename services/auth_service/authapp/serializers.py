from rest_framework import serializers

class GoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField()


class PatientSerializer(serializers.Serializer):
    patient_id = serializers.CharField()