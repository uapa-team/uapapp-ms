from django.db import models
from rest_framework import serializers

### Modelo de Vista que recolecta la información de las vistas creadas en la base de datos
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

class ReportTypes(models.TextChoices):
    REPORTE = 'RE'
    FORMATO_DE_RECOLECCION = 'FR'

class ReportLevels(models.TextChoices):
    PREGRADO = 'PRE'
    POSGRADO = 'POS'
    NO_APLICA = 'NA'

class Format(models.TextChoices):
    ADMITIDOS = 'Admitidos'
    DOCENTES = 'Docentes'
    EGRESADOS = 'Egresados'
    ESTUDIANTES = 'Estudiantes'
    GENERALES = 'Generales'
    INVESTIGACION = 'Investigacion'
    PROGRAMA = 'Programa'
    NO_APLICA = 'NA'

class Period(models.Model):
    class Meta:
        ordering = ['-code']
    code = models.IntegerField(primary_key=True, verbose_name='Codigo')
    text = models.CharField(max_length=10, verbose_name='Texto')

    def __str__(self):
        return self.text

### Modelo de Reporte el cual abstrae la información de los reportes y Formatos de Recoleccion
class Report(models.Model):
    class Meta:
        ordering = ['category', 'name']

    name = models.CharField(unique=True, max_length=50, verbose_name='Nombre del reporte')
    description = models.TextField(verbose_name='Descripción', default='')

    category = models.TextField(verbose_name='Categoria',
        choices=ReportTypes.choices, default=ReportTypes.REPORTE)
    level = models.TextField(verbose_name='Nivel',
        choices=ReportLevels.choices, default=ReportLevels.NO_APLICA,
        help_text='Nivel de la información')
    _format = models.TextField(verbose_name='Formato', 
        choices=Format.choices, default=Format.NO_APLICA,
        help_text='Solo aplica en el caso de los formatos de recolección')
    periods = models.ManyToManyField(Period, blank=True, verbose_name='Periodos')

    def __str__(self):
        return self.name

### Modelo que relaciona vistas y reportes
class ReportViewRelation(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    view = models.ForeignKey(View, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.view)
