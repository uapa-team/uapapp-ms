from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.check, name='check'),
    path('login', views.login, name='login'),
    path('refresh', views.refresh, name='refresh'),

    path('reports', views.reports, name='reports'),
    path('report/<int:code>', views.report, name='reports'),

    path('formats', views.formats, name='formats'),
    path('subformats/<str:fr>', views.subformats, name='subformats'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)