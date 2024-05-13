from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.ModelForm):
  class Meta:
    model  = User
    fields = ('username', 'password')
    help_texts = { 'username': None }
    widgets = {
      'username': forms.TextInput(attrs={
        'id': 'login-username',
        'class': 'form-control',
        'placeholder': 'username',
        'required': True
      }),
      'password': forms.PasswordInput(attrs={
        'id': 'login-password',
        'class': 'form-control',
        'placeholder': 'password',
        'required': True
      }),
    }
class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Email')



class NewPasswordForm(forms.Form):
    password = forms.CharField(label='New Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)