from django.db import models

# Create your models here.

class Client(models.Model):
    client_name = models.CharField(max_length=100)
    client_contact = models.CharField(max_length=100)
    client_info = models.TextField(max_length=200)

    objects = models.Manager()
    
    def __str__(self):
        return self.client_name