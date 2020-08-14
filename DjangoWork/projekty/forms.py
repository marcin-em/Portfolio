from django import forms
from .models import Project

from django.forms import SelectDateWidget


#class DateInput(forms.DateInput):
#    input_type = 'date'

class ProjectModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProjectModelForm, self).__init__(*args, **kwargs)
        self.fields['project_info'].required = False   
    
    class Meta:
        model = Project
        fields = [
            'client_name',
            'project_name',
            'project_start_date',
            'project_status',
            'project_info',
        ]
        widgets = {
            #'project_start_date': DateInput(),
            'project_start_date' : SelectDateWidget(),
        }
