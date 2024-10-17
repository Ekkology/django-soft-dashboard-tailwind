from django.db import models

class Event(models.Model):
    nombre = models.CharField(max_length=100)
    fecha = models.DateField()
    configuracion = models.JSONField(default=dict, blank=True, null=True)  # Asegúrate de usar el campo correcto
    def __str__(self):
        return self.nombre


class Chair(models.Model):
    numero = models.IntegerField()
    evento = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='chairs', null=True)

    def __str__(self):
        return f'chair {self.numero}'