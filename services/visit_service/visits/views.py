from django.shortcuts import render
from rest_framework import generics
from .models import TimeSlot
from .serializers import TimeSlotSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="Pobierz dostępne time sloty",
    description="Zwraca wszystkie dostępne przedziały czasowe dla wszystkich lekarzy.",
    responses=TimeSlotSerializer(many=True),
)
class TimeSlotListView(generics.ListAPIView):
    queryset = TimeSlot.objects.filter(is_available=True)
    serializer_class = TimeSlotSerializer
