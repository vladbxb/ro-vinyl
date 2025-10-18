from django.db import models
import uuid

# Create your models here.

class Locatie(models.Model):
    adresa = models.CharField(max_length=255)
    oras = models.CharField(max_length=100)
    judet = models.CharField(max_length=100)
    cod_postal = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.adresa}, {self.oras}"