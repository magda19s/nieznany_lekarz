from django.db import models
import uuid
from django.utils import timezone

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    visit_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')], default='unpaid')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    currency = models.CharField(max_length=10, default='PLN')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.id} ({self.status})"

