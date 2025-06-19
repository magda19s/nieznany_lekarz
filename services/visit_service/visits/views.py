from django.shortcuts import render
from rest_framework import generics
from .models import TimeSlot,Visit
from .serializers import TimeSlotSerializer, VisitCreateSerializer, VisitSerializer, VisitNotesUpdateSerializer, VisitStatusUpdateSerializer, PatientSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
from rest_framework.views import APIView
from rest_framework.response import Response
import uuid
from rest_framework import status
import requests
from django.conf import settings
from .utils.rabbitmq_publisher import publish_visit_booked_event
from .utils.notes_publisher import publish_visit_notes_event
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
import jwt
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import OpenApiResponse


@extend_schema(
    summary="Retrieve available time slots",
    description="Returns all available time slots for all doctors.",
    responses={200: TimeSlotSerializer},
)
class TimeSlotListView(generics.ListAPIView):
    queryset = TimeSlot.objects.filter(is_available=True)
    serializer_class = TimeSlotSerializer


@extend_schema(
    summary="Create a new visit",
    description="Creates a new visit for a patient.",
    parameters=[
        OpenApiParameter(
            name='timeslot_id',
            description='Timeslot fo the visit',
            required=True,
            type=str,
            location=OpenApiParameter.PATH,
        )
    ],
    responses={201: VisitSerializer},
    )
class VisitCreateView(generics.GenericAPIView):
    def post(self, request, timeslot_id):
        patient = request.user
        patient_id = getattr(patient, 'id', None)
        if not patient_id:
            return Response({"detail": "Patient ID not found in token"}, status=401)

        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            return Response({"detail": "Authorization header missing"}, status=401)

        try:
            url = f"{settings.AUTH_SERVICE_URL}/auth/patient"
            headers = {
            "Authorization": auth_header
            }    
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code != 200 or response.text.lower() != 'true':
                return Response({"detail": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
        except requests.RequestException:
            return Response({"detail": "Failed to contact user service"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        try:
            time_slot = TimeSlot.objects.get(id=timeslot_id)
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

        print("[DEBUG] About to publish event for visit:", visit.id)
        publish_visit_booked_event(visit)
        print("[DEBUG] Event publish call finished.")

        return Response({
            "id": visit.id,
            "doctor_id": visit.doctor.doctor_id,
            "patient_id": visit.patient_id,
            "time_slot": time_slot.id,
            "status": visit.status,
            "notes": visit.notes
        }, status=status.HTTP_201_CREATED)

    

@extend_schema(
    summary="Retrieve patient's visits",
    description="Returns a list of visits assigned to the authenticated patient.",
    responses={200: VisitSerializer(many=True)},
)
class VisitByPatientView(generics.ListAPIView):
    serializer_class = VisitSerializer

    def get_queryset(self):
        # tutaj odwołujemy się do self.request.user
        patient = self.request.user
        patient_id = getattr(patient, "id", None)
        if not patient_id:
            return Visit.objects.none()
        return Visit.objects.filter(patient_id=patient_id)

    def list(self, request, *args, **kwargs):
        patient_id = getattr(request.user, "id", None)
        if not patient_id:
            return Response(
                {"detail": "Patient ID not found in token"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        return super().list(request, *args, **kwargs)

@extend_schema(
    summary="Retrieve doctor's visits",
    description="Returns a list of visits assigned to the authenticated doctor.",
    responses={200: VisitSerializer(many=True)},
)
class VisitByDoctorView(generics.ListAPIView):
    serializer_class = VisitSerializer

    def get_queryset(self):
        doctor = self.request.user
        doctor_id = getattr(doctor, "id", None)
        if not doctor_id:
            return Visit.objects.none()
        return Visit.objects.filter(doctor__doctor_id=doctor_id)

    def list(self, request, *args, **kwargs):
        doctor_id = getattr(request.user, "id", None)
        if not doctor_id:
            return Response(
                {"detail": "Doctor ID not found in token"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return super().list(request, *args, **kwargs)
    
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

    def patch(self, request, visit_id):
        serializer = VisitNotesUpdateSerializer(data=request.data)
        if serializer.is_valid():
            notes = serializer.validated_data['notes']

            try:
                visit = Visit.objects.get(id=visit_id)
            except Visit.DoesNotExist:
                return Response({"detail": "Visit not found"}, status=status.HTTP_404_NOT_FOUND)

            doctor = request.user
            doctor_id = getattr(doctor, 'id', None)
            if not doctor_id:
                return Response({"detail": "Doctor ID not found in token"}, status=401)
            if visit.doctor.doctor_id != doctor_id:
                return Response({"detail": "This doctor is not assigned to the visit."}, status=status.HTTP_403_FORBIDDEN)

            visit.notes = notes
            publish_visit_notes_event(visit)

            visit.save()

            return Response(VisitSerializer(visit).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@extend_schema(
    summary="Update visit status",
    parameters=[
        OpenApiParameter(
            name='visit_id',
            description='ID of the visit',
            required=True,
            type=str,
            location=OpenApiParameter.PATH,
        )
    ],
    request=VisitStatusUpdateSerializer,
    responses={
        200: VisitSerializer,
        403: {"detail": "Forbidden"},
        404: {"detail": "Visit not found"},
    }
)
class UpdateVisitStatusView(APIView):
    def patch(self, request, visit_id):
        status_value = request.data.get('status')

        if status_value not in ['paid', 'unpaid']:
            return Response({"detail": "Invalid status. Allowed: 'paid' or 'unpaid'."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            visit = Visit.objects.get(id=visit_id)
        except Visit.DoesNotExist:
            return Response({"detail": "Visit not found"}, status=status.HTTP_404_NOT_FOUND)

        if status_value == 'paid':
            visit.status = 'paid'
        elif status_value == 'unpaid':
            visit.status = 'cancelled'

        visit.save()
        return Response({"detail": f"Visit status updated to '{visit.status}'"}, status=status.HTTP_200_OK)
    
@extend_schema(
    summary="Retrieve patient data from Auth Service",
    description="Fetches patient details from the external Auth Service based on patient ID.",
    parameters=[
        OpenApiParameter(
            name='patient_id',
            description='UUID of the patient',
            required=True,
            type=str,
            location=OpenApiParameter.PATH,
        ),
    ],
    responses={
        200: PatientSerializer,
        404: {"detail": "Patient not found"},
        401: {"detail": "Authorization header missing"},
        503: {"detail": "Failed to contact auth service"},
    }
)
class PatientRetrieveView(generics.GenericAPIView):
    serializer_class = PatientSerializer

    def get(self, request, patient_id):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if not auth_header:
            return Response({"detail": "Authorization header missing"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            url = f"{settings.AUTH_SERVICE_URL}/auth/patient/{patient_id}"
            headers = {"Authorization": auth_header}
            response = requests.get(url, headers=headers, timeout=5)

            if response.status_code == 200:
                return Response(response.json(), status=status.HTTP_200_OK)
            elif response.status_code == 404:
                return Response({"detail": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"detail": "Unexpected response from auth service"}, status=status.HTTP_502_BAD_GATEWAY)

        except requests.RequestException as e:
            return Response({"detail": "Failed to contact auth service", "error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)


    

