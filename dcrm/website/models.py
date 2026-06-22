from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLES = (
        ('administrador', 'Administrador'),
        ('usuario', 'Usuario/Pasajero'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='usuario')

class Station(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Report(models.Model):
    PROBLEM_TYPES = (
        ('tecnico', 'Fallo Técnico'),
        ('sugerencia', 'Sugerencia de Mejora'),
        ('otro', 'Otro'),
    )
    STATUS_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('validado', 'Validado'),
        ('descartado', 'Descartado'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    problem_type = models.CharField(max_length=20, choices=PROBLEM_TYPES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendiente')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_problem_type_display()} - {self.status}"

class GlobalNotification(models.Model):
    message = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.message[:50]
