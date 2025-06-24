from django.contrib.auth.forms import UserCreationForm
from django import forms

from account.models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'username', 'password1', 'password2')
        

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'username', 'avatar')