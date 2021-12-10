from django.contrib.auth import forms
from .models import User

from django.forms import ModelForm, Textarea, NumberInput
from django.utils.translation import gettext_lazy as _
from .models import *


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User

class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User

class CoordenadorCursoForm(ModelForm):
    class Meta:
        fields = ['username', 'email', 'first_name', 'last_name', 'telefone', 'password', 'tipo_usuario']
        model = User

