from django.contrib import admin
from .models import Report, View, ReportViewRelation

class ReportViewInLine(admin.StackedInline):
    model = ReportViewRelation
    extra = 1

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    inlines = [ReportViewInLine]

@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'sheet_name')
        }),
        ('Filtros', {
            'fields': ('main_period', 'main_program'),
            'description': 'Nombre de las columnas para filtrar (dejar en blanco para ignorar).'
        })
    )
