from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import pytz
from .models import Payment
from .utils.rabbitmq_publisher import publish_payment_event
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from payments.models import Payment
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
import os
from datetime import datetime
import pytz

utc = pytz.UTC
local_tz = pytz.timezone("Europe/Warsaw")

STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
FRONTEND_URL = os.environ.get("FRONTEND_URL")

@extend_schema(exclude=True) 
class StripeWebhookView(APIView):

    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header,
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

            payment.status = 'paid'
            payment.updated_at = datetime.now(pytz.timezone('Europe/Warsaw'))
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
        stripe.api_key = STRIPE_SECRET_KEY
        serializer = TimeSlotPayloadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if not FRONTEND_URL:
            return Response({"detail": "Missing FRONTEND_URL in settings"}, status=500)
        
        user = request.user
        user_id = getattr(user, 'id', None)
        
        if not user_id:
            return Response({"detail": "User ID not found in token"}, status=401)
        
        timeslot = serializer.validated_data
        doctor = timeslot["doctor"]
        start_raw = timeslot['start']
        start_dt = datetime.strptime(start_raw, "%Y-%m-%dT%H:%M:%SZ")
        formatted_start = start_dt.strftime("%d %B %Y, %H:%M")
        price = float(doctor["amount"])

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
                                "name": f"Payment for a visit in Nieznany Lekarz, {formatted_start}",
                                "description": f"Doctor: {doctor['first_name']} {doctor['last_name']} ({doctor['specialization']})",
                            },
                            "unit_amount": int(price * 100),
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                ui_mode="embedded",
                return_url=f"{FRONTEND_URL}/payment/redirect?session_id={{CHECKOUT_SESSION_ID}}",
                metadata=metadata,
                payment_intent_data={"metadata": metadata},
            )

            return Response({"client_secret": session.client_secret}, status=200)

        except Exception as e:
            return Response(
                {"detail": f"Stripe error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@extend_schema(
    summary="Get payment status from Stripe session ID",
    description="Fetches payment status based on session ID after redirect from Stripe.",
    parameters=[
        OpenApiParameter(
            name='session_id',
            description='Stripe Checkout session ID',
            required=True,
            type=str,
            location=OpenApiParameter.PATH,
        )
    ],
    responses={200: dict, 404: {"detail": "Session not found"}}
)
class StripePaymentStatusView(APIView):
    def get(self, request, session_id):
        stripe.api_key = STRIPE_SECRET_KEY

        try:
            session = stripe.checkout.Session.retrieve(session_id)
            status_value = session.get("payment_status")
            metadata = session.get("metadata", {})
            visit_id = metadata.get("timeslot_id")
            return Response({
                "status": status_value,
                "visit_id": visit_id,
                "metadata": metadata,
            }, status=200)

        except stripe.error.InvalidRequestError:
            return Response({"detail": "Session not found"}, status=404)
