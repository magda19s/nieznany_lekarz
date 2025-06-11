from django.urls import path
from .views import TimeSlotListView, VisitCreateView, VisitByDoctorView, VisitByPatientView, UpdateVisitNotesView, UpdateVisitStatusView,PatientRetrieveView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('timeslots/', TimeSlotListView.as_view(), name='timeslot-list'),
    path('visits/<str:timeslot_id>', VisitCreateView.as_view(), name='visit-create'),
    path('visits/patient/', VisitByPatientView.as_view(), name='visit-patient'),
    path('visits/doctor/', VisitByDoctorView.as_view(), name='visit-doctor'),
    path('visits/<str:visit_id>/doctor/', UpdateVisitNotesView.as_view(), name='visit-doctor'),
    path('visits/<str:visit_id>/', UpdateVisitStatusView.as_view(), name='visit-payment'),
    path('patient/<str:patient_id>/', PatientRetrieveView.as_view(), name='get-patient'),

      # Swagger / OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]