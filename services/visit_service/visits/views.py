from django.shortcuts import render
from rest_framework import generics
from .models import TimeSlot,Visit
from .serializers import TimeSlotSerializer, VisitCreateSerializer, VisitSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
import uuid



@extend_schema(
    summary="Pobierz dostępne time sloty",
    description="Zwraca wszystkie dostępne przedziały czasowe dla wszystkich lekarzy.",
    responses=TimeSlotSerializer(many=True),
)
class TimeSlotListView(generics.ListAPIView):
    queryset = TimeSlot.objects.filter(is_available=True)
    serializer_class = TimeSlotSerializer


@extend_schema(
    summary="Utwórz nową wizytę",
    description="Tworzy nową wizytę dla pacjenta.",
    responses={201: VisitSerializer},
    )
class VisitCreateView(generics.GenericAPIView):
    serializer_class = VisitCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            time_slot_id = serializer.validated_data['time_slot_id']
            patient_id = serializer.validated_data['patient_id']

            try:
                time_slot = TimeSlot.objects.get(id=time_slot_id)
            except TimeSlot.DoesNotExist:
                return Response({"detail": "Time slot not found"}, status=status.HTTP_404_NOT_FOUND)

            if not time_slot.is_available:
                return Response({"detail": "This time slot is already booked"}, status=status.HTTP_400_BAD_REQUEST)

            visit = Visit.objects.create(
                id=str(uuid.uuid4()),
                doctor=time_slot.doctor,
                patient_id=patient_id,
                time_slot=time_slot,
                status='booked',
                notes=request.data.get('notes', '')
            )
            time_slot.is_available = True
            time_slot.save()

            return Response({
                "id": visit.id,
                "doctor_id": visit.doctor.doctor_id,
                "patient_id": visit.patient_id,
                "time_slot": time_slot.id,
                # "status": visit.status,
                "notes": visit.notes
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)