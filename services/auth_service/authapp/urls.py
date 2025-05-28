from django.urls import path
from .views import GoogleAuthView, CheckPatientExistsView, UserDetailView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("auth/google", GoogleAuthView.as_view(), name="google-auth"),
    path("auth/patient/<str:patient_id>", CheckPatientExistsView.as_view(), name="check-patient"),
    path("auth/user/<str:user_id>", UserDetailView.as_view(), name="check-user"),
      # Swagger / OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
