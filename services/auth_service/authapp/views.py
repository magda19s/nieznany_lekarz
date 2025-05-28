from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import User  # Zakładam, że masz taki model
from .serializers import GoogleAuthSerializer, GoogleSerializer, UserSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from .utils.doctor_publisher import publish_register_doctor_event

@extend_schema(
    summary="Authenticate user with Google",
    description="Weryfikuje użytkownika przy użyciu tokena Google (credential). Jeśli użytkownik nie istnieje, zostaje utworzony. Domyślnie z rolą `pacjent`, chyba że jego e-mail znajduje się na liście lekarzy.",
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "credential": {"type": "string", "description": "Google ID token z frontendu"},
            },
            "required": ["credential"]
        }
    },
    responses={
    200: GoogleSerializer,
    400: {"detail": "Invalid Google token"},
    }
)
class GoogleAuthView(APIView):
    def post(self, request):
        credential_token = request.data.get("credential")

        if not credential_token:
            return Response({"detail": "Missing credential token"}, status=status.HTTP_400_BAD_REQUEST)

        try:

            idinfo = id_token.verify_oauth2_token(
                credential_token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )

            # Dane z tokenu
            email = idinfo.get("email")
            first_name = idinfo.get("given_name", "")
            last_name = idinfo.get("family_name", "")
            user_id = idinfo.get("sub")  # Google ID (unikalny)

            print(settings.DOCTOR_EMAILS, "EMAILS")
            # Czy użytkownik istnieje?
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "id": user_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "role": "lekarz" if email in settings.DOCTOR_EMAILS else "pacjent"
                }
            )

            if user.role == 'lekarz':
                publish_register_doctor_event(user)

            tokens = get_tokens_for_user(user)

            return Response({
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                },
                "created": created,
                "access_token": tokens["access_token"],
                "refresh": tokens["refresh"]
            }, status=status.HTTP_200_OK)

        except ValueError:
           return Response({"detail": "Invalid Google token"}, status=status.HTTP_400_BAD_REQUEST)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access_token": str(refresh.access_token),
    }
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
        

class UserDetailView(APIView):
    # Ten endpoint służy do pobrania danych usera po jego id (np. z tokena)
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)