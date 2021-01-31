from django.db import models
from rest_framework import serializers

class View(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=50, verbose_name='Vista a consultar', unique=True,
        help_text='Nombre de la vista en la base de datos')
    sheet_name = models.CharField(max_length=50, verbose_name='Nombre de la hoja',
        help_text='Nombre de la hoja creada')

    main_period = models.CharField(max_length=50, verbose_name='Columna de código periodo',
        default = None, blank=True,
        help_text='Columna con los códigos de periodo en la vista para filtrar')
    text_period = models.CharField(max_length=50, verbose_name='Columna de nombre periodo',
        default = None, blank=True,
        help_text='Columna con los nombres de periodo para mostrar')

    main_program = models.CharField(max_length=50, verbose_name='Columna de código programa',
        default = None, blank=True,
        help_text='Columna con los códigos de programa en la vista para filtrar')
    text_program = models.CharField(max_length=50, verbose_name='Columna de nombre programa',
        default = None, blank=True,
        help_text='Columna con los nombres de programa para mostrar')
    
    def __str__(self):
        return self.name

class Report(models.Model):
    class Meta:
        ordering = ['name']
    
    name = models.CharField(unique=True, max_length=50, verbose_name='Nombre del reporte')
    description = models.TextField(verbose_name='Descripción', default='')

    def __str__(self):
        return self.name

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['name']

class ReportViewRelation(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    view = models.ForeignKey(View, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.view)
