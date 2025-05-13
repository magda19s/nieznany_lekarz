from django.db import models

class Payment(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    visit_id = models.CharField(max_length=100)
    status = models.CharField(max_length=10, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')])

    def __str__(self):
        return f"{self.id} ({self.status})"

