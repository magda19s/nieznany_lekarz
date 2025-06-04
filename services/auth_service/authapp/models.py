from django.db import models

class User(models.Model):
    # Identyfikator użytkownika
    id = models.CharField(primary_key=True, max_length=100)
    
    # Adres e-mail, unikalny
    email = models.EmailField(unique=True)
    
    # Imię użytkownika
    first_name = models.CharField(max_length=100)
    
    # Nazwisko użytkownika
    last_name = models.CharField(max_length=100)
    
    # Rola użytkownika (lekarz lub pacjent)
    role = models.CharField(max_length=50, choices=[
    ('doctor', 'Doctor'),
    ('patient', 'Patient'),
])

    def __str__(self):
        # Zwróć pełne imię i nazwisko oraz rolę użytkownika
        return f"{self.first_name} {self.last_name} - {self.role}"
