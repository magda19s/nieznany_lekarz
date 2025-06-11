from django.urls import path
from .views import GoogleAuthView, CheckPatientExistsView, UserDetailView,GetUserByIdView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("auth/google", GoogleAuthView.as_view(), name="google-auth"),
    path("auth/patient", CheckPatientExistsView.as_view(), name="check-patient"),
    path("auth/user", UserDetailView.as_view(), name="check-user"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('auth/patient/<str:user_id>/', GetUserByIdView.as_view(), name='get-user-by-id'),
    
    # Swagger / OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]