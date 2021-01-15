from django.db import models

# Create your models here.

class Report(models.Model):
    name = models.CharField(unique=True, max_length=50, verbose_name='Nombre del reporte')

class View(models.Model):
    report_name = models.ForeignKey(Report, on_delete=models.CASCADE)
    view = models.CharField(max_length=50, verbose_name='Vistas a consultar')
    