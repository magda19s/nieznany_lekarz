from rest_framework import generics, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from django.core.mail import send_mail
from .serializers import SendEmailSerializer

@extend_schema(
    summary="Send an email",
    description="Sends an email using provided subject, message and recipient.",
    request=SendEmailSerializer,
    responses={
        200: OpenApiResponse(description="Email sent successfully."),
        400: OpenApiResponse(description="Validation failed."),
        500: OpenApiResponse(description="Sending email failed."),
    },
)
class SendEmailView(generics.GenericAPIView):
    serializer_class = SendEmailSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        subject = serializer.validated_data['subject']
        message = serializer.validated_data['message']
        recipient = serializer.validated_data['recipient']

        try:
            send_mail(
                subject,
                message,
                'twoj.email@gmail.com',
                [recipient],
                fail_silently=False,
            )
            return Response({"detail": "Email sent successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "detail": "Email send failed",
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
