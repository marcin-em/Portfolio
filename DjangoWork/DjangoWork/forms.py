from django import forms
from django.contrib.auth import authenticate


class UserLoginForm(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    username = forms.CharField(label=False)
    password = forms.CharField(widget=forms.PasswordInput, label=False)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('Nieprawidłowa nazwa użytkownika lub hasło')
        return super(UserLoginForm, self).clean(*args, **kwargs)
    
