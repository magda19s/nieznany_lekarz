from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role')  # To, co będzie wyświetlane na liście
    search_fields = ('email', 'first_name', 'last_name', 'role')  # Możliwość wyszukiwania
    list_filter = ('role',)  # Możliwość filtrowania po roli

# Rejestracja modelu w adminie
admin.site.register(User, UserAdmin)
