from drf_spectacular.extensions import OpenApiAuthenticationExtension

class CustomJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'authapp.customJwt.SimpleJWTWithoutDBUser'
    name = 'BearerAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }