from django.contrib import admin
from .models import Report, View, ReportViewRelation, Period

class ReportViewInLine(admin.StackedInline):
    model = ReportViewRelation
    extra = 1

admin.site.register(Period)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    inlines = [ReportViewInLine,]
    filter_horizontal = ('periods',)

@admin.register(View)
class ViewAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'sheet_name')
        }),
        ('Filtros', {
            'fields': ('main_period', 'text_period', 'main_program', 'text_program'),
            'description': 'Nombre de las columnas para filtrar (dejar en blanco para ignorar).'
        })
    )
