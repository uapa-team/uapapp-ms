from django.urls import path

from . import views

urlpatterns = [
    path('', views.check, name='check'),
    path('login', views.login, name='login'),
]