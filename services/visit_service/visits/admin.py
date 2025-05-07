from django.contrib import admin
from .models import Doctor, TimeSlot, Visit

admin.site.register(Doctor)
admin.site.register(TimeSlot)
admin.site.register(Visit)