from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class GoogleAuthSerializer(serializers.Serializer):
    token = serializers.CharField()


class PatientSerializer(serializers.Serializer):
    patient_id = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role']    

class GoogleSerializer(serializers.Serializer):
    user = UserSerializer()
    created = serializers.CharField()
    access_token = serializers.CharField()
    refresh = serializers.CharField()

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['user_id'] = str(self.user.id)
        data['email'] = self.user.email
        data['role'] = self.user.role
        return data
