from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import CreateCheckoutSessionView, StripeWebhookView, StripePaymentStatusView


urlpatterns = [
      # Swagger / OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    # path('payment/<str:visit_id>/', PaymentStatusUpdateView.as_view(), name='payment-update'),
    path('payments/webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path('payment/status/<str:session_id>/', StripePaymentStatusView.as_view(), name='payment-status'),
    
    path("checkout/", CreateCheckoutSessionView.as_view(), name="create-checkout"),

]