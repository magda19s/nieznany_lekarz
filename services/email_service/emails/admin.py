from django.contrib import admin
from .models import Email

@admin.register(Email)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('to', 'subject', 'status', 'sent_at')
    search_fields = ('to', 'subject', 'status')
    readonly_fields = ('to', 'subject', 'message', 'status', 'error_message', 'sent_at')
