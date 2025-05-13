from django.urls import path
from .views import GoogleAuthView, CheckPatientExistsView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("auth/google", GoogleAuthView.as_view(), name="google-auth"),
    path("auth/patient/<str:patient_id>", CheckPatientExistsView.as_view(), name="check-patient"),
      # Swagger / OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
