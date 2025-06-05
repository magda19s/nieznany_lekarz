from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import CreateCheckoutSessionView, PaymentStatusUpdateView, StripeWebhookView


urlpatterns = [
      # Swagger / OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('payment/<str:visit_id>/', PaymentStatusUpdateView.as_view(), name='payment-update'),
    path('payment/stripe/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path("checkout/", CreateCheckoutSessionView.as_view(), name="create-checkout"),

]