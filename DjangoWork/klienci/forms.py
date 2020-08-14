from django import forms
from .models import Client

from django.forms import SelectDateWidget

class ClientModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClientModelForm, self).__init__(*args, **kwargs)
        self.fields['client_info'].required = False

    class Meta:
        model = Client
        fields = [
            'client_name',
            'client_contact',
            'client_info',
        ]
    
    def clean_client_name(self, *args, **kwargs):
        instance = self.instance
        client_name = self.cleaned_data.get('client_name')
        qs = Client.objects.filter(client_name=client_name)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise forms.ValidationError('Klient już istnieje')
        return client_name
