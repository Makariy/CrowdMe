from django import forms

from .models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('name', 'password', 'mail')



