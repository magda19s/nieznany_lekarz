from drf_spectacular.extensions import OpenApiAuthenticationExtension

class CustomJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'visits.customJwt.SimpleJWTWithoutDBUser'  # pełna ścieżka do Twojej klasy
    name = 'BearerAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }