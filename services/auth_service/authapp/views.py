from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import User  # Zakładam, że masz taki model
from .serializers import GoogleAuthSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

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

@extend_schema(
    summary="Check if patient exists",
    description="Returns true if a user with the given ID exists and has the role 'patient'; otherwise, returns false.",
    parameters=[
        OpenApiParameter(
            name='patient_id',
            description='Verify patient existence',
            required=True,
            type=str,
            location=OpenApiParameter.PATH,
        )
    ],
    responses={200: bool, 404: bool}
)
class CheckPatientExistsView(generics.GenericAPIView):
    def get(self, request, patient_id):
        try:
            user = User.objects.get(id=patient_id)
            if user.role == 'pacjent':
                return Response(True, status=status.HTTP_200_OK)
            return Response(False, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(False, status=status.HTTP_404_NOT_FOUND)