from django.db import models
from klienci.models import Client
from django import forms
from django.conf import settings
from django.utils import timezone

# Create your models here.

User = settings.AUTH_USER_MODEL


class Project(models.Model):
    
    #client_name = forms.ModelChoiceField(queryset=Client.objects.values('client_name'))
    PROJECT_OPEN = 'Otwarty'
    PROJECT_CLOSED = 'Zamknięty'
    PROJECT_STATUS = [
        (PROJECT_OPEN, 'otwarty'),
        (PROJECT_CLOSED, 'zamknięty')
    ]

    project_name = models.CharField(max_length=100)
    client_name = models.ForeignKey(Client, null=True, on_delete=models.CASCADE)
    project_start_date = models.DateField(default=timezone.now)
    project_create_date = models.DateField(auto_now_add=True, blank=True)
    project_status = models.CharField(max_length=10, choices=PROJECT_STATUS, default=PROJECT_OPEN)
    project_info = models.TextField(max_length=200)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    objects = models.Manager()