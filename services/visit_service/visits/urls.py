from django.urls import path
from .views import TimeSlotListView, VisitCreateView, VisitByDoctorView, VisitByPatientView, UpdateVisitNotesView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('timeslots/', TimeSlotListView.as_view(), name='timeslot-list'),
    path('visits/', VisitCreateView.as_view(), name='visit-create'),
    path('visits/patient/<str:patient_id>/', VisitByPatientView.as_view(), name='visit-patient'),
    path('visits/doctor/<str:doctor_id>/', VisitByDoctorView.as_view(), name='visit-doctor'),
    path('visits/<str:visit_id>/doctor/<str:doctor_id>/', UpdateVisitNotesView.as_view(), name='visit-doctor'),

      # Swagger / OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]