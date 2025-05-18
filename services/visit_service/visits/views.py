from django.shortcuts import render
from rest_framework import generics
from .models import TimeSlot,Visit
from .serializers import TimeSlotSerializer, VisitCreateSerializer, VisitSerializer, VisitNotesUpdateSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
from rest_framework.views import APIView
from rest_framework.response import Response
import uuid
from rest_framework import status
import requests
from django.conf import settings
from .utils.rabbitmq_publisher import publish_visit_booked_event
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes, authentication_classes



@extend_schema(
    summary="Retrieve available time slots",
    description="Returns all available time slots for all doctors.",
    responses=TimeSlotSerializer(many=True),
)
class TimeSlotListView(generics.ListAPIView):
    queryset = TimeSlot.objects.filter(is_available=True)
    serializer_class = TimeSlotSerializer


@extend_schema(
    summary="Create a new visit",
    description="Creates a new visit for a patient.",
    responses={201: VisitSerializer},
    )
@permission_classes([AllowAny])
class VisitCreateView(generics.GenericAPIView):
    permission_classes = [AllowAny] 
    serializer_class = VisitCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            time_slot_id = serializer.validated_data['time_slot_id']
            patient_id = serializer.validated_data['patient_id']

            try:
                # URL mikroserwisu User Service (można dać do settings!)
                url = f"{settings.AUTH_SERVICE_URL}/auth/patient/{patient_id}"
                response = requests.get(url, timeout=5)
                print(response)
                if response.status_code != 200 or response.text.lower() != 'true':
                    return Response({"detail": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
            except requests.RequestException as e:
                return Response({"detail": "Failed to contact user service"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


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
            time_slot.is_available = False
            time_slot.save()

            publish_visit_booked_event(visit)

            return Response({
                "id": visit.id,
                "doctor_id": visit.doctor.doctor_id,
                "patient_id": visit.patient_id,
                "time_slot": time_slot.id,
                "status": visit.status,
                "notes": visit.notes,
                'variant': visit.variant
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@extend_schema(
    summary="Retrieve patient's visits",
    description="Returns a list of visits assigned to a patient based on their ID.",
    parameters=[
        OpenApiParameter(
            name='patient_id',
            description="ID of the patient whose visits you want to retrieve",
            required=True,
            type=str,
            location=OpenApiParameter.PATH,
        )
    ],
    responses={200: VisitSerializer(many=True)},
)
class VisitByPatientView(generics.ListAPIView):
    serializer_class = VisitSerializer

    def get_queryset(self):
        patient_id = self.kwargs['patient_id']
        return Visit.objects.filter(patient_id=patient_id)

@extend_schema(
    summary="Retrieve doctor's visits",
    description="Returns a list of visits assigned to a doctor based on their ID.",
    parameters=[
        OpenApiParameter(
            name='doctor_id',
            description="ID of the doctor whose visits you want to retrieve",
            required=True,
            type=str,
            location=OpenApiParameter.PATH,
        )
    ],
    responses={200: VisitSerializer(many=True)},
)
class VisitByDoctorView(generics.ListAPIView):
    serializer_class = VisitSerializer

    def get_queryset(self):
        doctor_id = self.kwargs['doctor_id']
        return Visit.objects.filter(doctor__doctor_id=doctor_id)
    
@extend_schema(
    summary="Update visit notes",
    description="Allows the doctor to update notes for a selected visit.",
    parameters=[
        OpenApiParameter(
            name='visit_id',
            description='ID of the visit',
            required=True,
            type=str,
            location=OpenApiParameter.PATH,
        ),
        OpenApiParameter(
            name='doctor_id',
            description='ID of the doctor',
            required=True,
            type=str,
            location=OpenApiParameter.PATH,
        )
    ],
    request=VisitNotesUpdateSerializer,
    responses={
        200: VisitSerializer,
        403: {"detail": "Forbidden"},
        404: {"detail": "Visit not found"},
    }
)
class UpdateVisitNotesView(APIView):

    def patch(self, request, visit_id, doctor_id):
        serializer = VisitNotesUpdateSerializer(data=request.data)
        if serializer.is_valid():
            notes = serializer.validated_data['notes']

            try:
                visit = Visit.objects.get(id=visit_id)
            except Visit.DoesNotExist:
                return Response({"detail": "Visit not found"}, status=status.HTTP_404_NOT_FOUND)

            if visit.doctor.doctor_id != doctor_id:
                return Response({"detail": "This doctor is not assigned to the visit."}, status=status.HTTP_403_FORBIDDEN)

            visit.notes = notes
            visit.save()
            return Response(VisitSerializer(visit).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)