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
    
class EmailLog(models.Model):
    to_email = models.EmailField(null=True, blank=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=50)  # zwiększone max_length
    error_message = models.TextField(null=True, blank=True)  # na dłuższe opisy błędów
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email to {self.to_email} - {self.status}"

