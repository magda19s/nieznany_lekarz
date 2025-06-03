from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions

class SimpleJWTWithoutDBUser(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
        except KeyError:
            raise exceptions.AuthenticationFailed('User ID not found in token')

        # Zwracamy prosty obiekt z id lub AnonymousUser
        class SimpleUser:
            def __init__(self, id):
                self.id = id
                self.is_authenticated = True
            def __str__(self):
                return f"User({self.id})"

        return SimpleUser(user_id)
