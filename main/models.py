from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator,URLValidator

class Libro(models.Model):
    ISBN = models.IntegerField(primary_key = True)
    titulo = models.CharField(max_length=100)
    autor = models.CharField(max_length=100)
    anyoPublicacion = models.IntegerField(null=True)
    editor = models.CharField(max_length=100)
    def __str__(self):
        return self.titulo


class Puntuacion(models.Model):
    usuario = models.IntegerField(primary_key = True)
    ISBN = models.IntegerField()
    puntuacion = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    def __str__(self):
        return str(self.usuario)