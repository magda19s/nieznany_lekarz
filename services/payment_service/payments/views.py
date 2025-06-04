from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import pytz
from .models import Payment
from .serializers import PaymentStatusUpdateSerializer, PaymentSerializer
from .utils.rabbitmq_publisher import publish_payment_event
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from payments.models import Payment
from payments.serializers import PaymentSerializer  # zakładam, że to masz
from drf_spectacular.utils import extend_schema



@extend_schema(
    summary="Update payment status",
    description="Changes status after info from stripe",
    parameters=[
        OpenApiParameter(
            name='visit_id',
            description='ID of the visit',
            required=True,
            type=str,
            location=OpenApiParameter.PATH,
        )
    ],
    request=PaymentStatusUpdateSerializer,
    responses={
        200: PaymentSerializer,
        400: {"detail": "Invalid input"},
        404: {"detail": "Payment not found for this visit"},
    }
)
class PaymentStatusUpdateView(APIView):

    def patch(self, request, visit_id):
        serializer = PaymentStatusUpdateSerializer(data=request.data)
        if serializer.is_valid():
            new_status = serializer.validated_data['status']

            try:
                payment = Payment.objects.get(visit_id=visit_id)
            except Payment.DoesNotExist:
                return Response(
                    {"detail": "Payment not found for this visit"},
                    status=status.HTTP_404_NOT_FOUND
                )

            payment.status = new_status
            # payment.updated_at = datetime.now(pytz.timezone('Europe/Warsaw')).strftime("%d.%m.%Y %H:%M:%S")
            print("Publishing payment:", payment.id)

            payment.save()
            print("Publishing payment:", payment.id)
            publish_payment_event(payment)

            return Response(PaymentSerializer(payment).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@extend_schema(exclude=True) 
class StripeWebhookView(APIView):

    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, #webhook z env
            )
        except (ValueError, stripe.error.SignatureVerificationError):
            return Response({"detail": "Invalid payload or signature"}, status=status.HTTP_400_BAD_REQUEST)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']

            visit_id = session['metadata'].get('visit_id')
            if not visit_id:
                return Response({"detail": "visit_id not provided in metadata"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                payment = Payment.objects.get(visit_id=visit_id)
            except Payment.DoesNotExist:
                return Response({"detail": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

            payment.status = 'paid'  # lub cokolwiek pasuje
            payment.save()

            publish_payment_event(payment)

        # Obsłuż inne eventy, jeśli chcesz...

        return Response({"status": "success"}, status=status.HTTP_200_OK)
