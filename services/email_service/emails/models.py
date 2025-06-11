from django.db import models

class Email(models.Model):
    to = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('SENT', 'Sent'),
        ('FAILED', 'Failed')
    ])
    error_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.sent_at} -> {self.to} [{self.status}]"
    
# models.py
from django.db import models

class ReminderLog(models.Model):
    visit_id = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reminder for visit {self.visit_id} sent to {self.email}"

