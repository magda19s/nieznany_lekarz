from rest_framework import serializers
from .models import Email
class SendEmailSerializer(serializers.Serializer):
    recipient = serializers.EmailField()
    subject = serializers.CharField()
    message = serializers.CharField()

class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Email
        fields = '__all__'