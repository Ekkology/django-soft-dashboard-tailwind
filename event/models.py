from django.db import models

class Event(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField()
    configuracion = models.JSONField(default=dict, blank=True, null=True)  # Asegúrate de usar el campo correcto
