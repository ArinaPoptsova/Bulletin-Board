from django import forms
from django.contrib.auth.forms import UserCreationForm

from sign.models import User


class VerificationForm(forms.Form):
    code = forms.CharField(max_length=6)


class CreateUserForm(UserCreationForm):
    # email = forms.EmailField(unique=True)

    class Meta:
        model = User
        fields = ('email', 'username')
