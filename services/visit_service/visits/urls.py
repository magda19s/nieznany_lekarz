from django.urls import path
from .views import TimeSlotListView, VisitCreateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('timeslots/', TimeSlotListView.as_view(), name='timeslot-list'),
    path('visits/', VisitCreateView.as_view(), name='visit-create'),

      # Swagger / OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]