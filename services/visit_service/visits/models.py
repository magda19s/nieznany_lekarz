from django.db import models

class Doctor(models.Model):
    doctor_id = models.CharField(primary_key=True, max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)

class TimeSlot(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    doctor =  models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    is_available = models.BooleanField(default=True)

class Visit(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient_id = models.CharField(max_length=100)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('paid', 'Paid')
    ])
    notes = models.TextField(blank=True, null=True)
