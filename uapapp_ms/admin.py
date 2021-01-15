from django.contrib import admin
from .models import Report, View

class ViewInLine(admin.StackedInline):
    model = View
    extra = 1

class ReportAdmin(admin.ModelAdmin):
    inlines = [ViewInLine]

admin.site.register(Report, ReportAdmin)