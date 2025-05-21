from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import pytz
from .models import Payment
from .serializers import PaymentStatusUpdateSerializer, PaymentSerializer


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
                payment = Payment.objects.get(visit__id=visit_id)
            except Payment.DoesNotExist:
                return Response(
                    {"detail": "Payment not found for this visit"},
                    status=status.HTTP_404_NOT_FOUND
                )

            payment.status = new_status
            payment.updated_at = datetime.now(pytz.timezone('Europe/Warsaw')).strftime("%d.%m.%Y %H:%M:%S")

            payment.save()

            return Response(PaymentSerializer(payment).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

