from rest_framework import serializers
from .models import User

class GoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField()


class PatientSerializer(serializers.Serializer):
    patient_id = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
     class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'created', 'access', 'refresh']    