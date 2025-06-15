import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_service.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

def create_service_user():
    User = get_user_model()
    username = 'visit-service-user'
    password = 'super-secure-password'  # zmień na silniejsze w produkcji

    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_password(password)
        user.is_active = True
        user.save()
        print(f"[+] Użytkownik serwisowy '{username}' utworzony.")
    else:
        print(f"[i] Użytkownik serwisowy '{username}' już istnieje.")

    refresh = RefreshToken.for_user(user)
    print(f"Access token: {str(refresh.access_token)}")
    print(f"Refresh token: {str(refresh)}")

if __name__ == "__main__":
    create_service_user()
