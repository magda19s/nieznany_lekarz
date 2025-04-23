from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User  # Zakładam, że masz taki model
from .serializers import GoogleAuthSerializer

class GoogleAuthView(APIView):
    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']

        # Pseudo-weryfikacja tokena (normalnie: weryfikacja tokena JWT od Google)
        # Zakładamy, że token to email dla uproszczenia demo
        email = token  
        user, created = User.objects.get_or_create(email=email, defaults={"role": "patient"})

        return Response({
            "accessToken": "fake-jwt-token",  # Zastąp prawdziwym tokenem JWT w przyszłości
            "user": {
                "id": str(user.id),
                "email": user.email,
                "role": user.role,
            }
        }, status=status.HTTP_200_OK)
