from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import pytz
from .models import Payment
from .serializers import CreateCheckoutSerializer, PaymentStatusUpdateSerializer, PaymentSerializer
from .utils.rabbitmq_publisher import publish_payment_event
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from payments.models import Payment
from payments.serializers import PaymentSerializer 
from drf_spectacular.utils import extend_schema
from decouple import config
from rest_framework.permissions import IsAuthenticated

STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY")
FRONTEND_URL = config("FRONTEND_URL")

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

        return Response({"status": "success"}, status=status.HTTP_200_OK)

from .serializers import TimeSlotPayloadSerializer

@extend_schema(
    summary="Create Stripe Checkout Session",
    description="Creates a Stripe checkout session based on timeslot payload and doctor price.",
    request=TimeSlotPayloadSerializer,
    responses={200: dict, 400: {"detail": "Invalid input"}}
)
class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = TimeSlotPayloadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        timeslot = serializer.validated_data
        doctor = timeslot["doctor"]
        price = float(doctor["amount"])  # from frontend

        stripe.api_key = settings.STRIPE_SECRET_KEY
        frontend_url = settings.FRONTEND_URL
        if not frontend_url:
            return Response({"detail": "Missing FRONTEND_URL in settings"}, status=500)
        
        user = request.user
        user_id = getattr(user, 'id', None)
        if not user_id:
            return Response({"detail": "User ID not found in token"}, status=401)

        metadata = {
            "user_id": user_id,
            "timeslot_id": timeslot["id"],
            "doctor_id": doctor["doctor_id"],
        }

        try:
            session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price_data": {
                            "currency": "pln",
                            "product_data": {
                                "name": f"Wizyta: {doctor['first_name']} {doctor['last_name']}"
                            },
                            "unit_amount": int(price * 100),
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                ui_mode="embedded",
                return_url=f"{frontend_url}/redirect?session_id={{CHECKOUT_SESSION_ID}}",
                metadata=metadata,
                payment_intent_data={"metadata": metadata},
            )

            return Response({"client_secret": session.client_secret}, status=200)

        except Exception as e:
            return Response(
                {"detail": f"Stripe error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
