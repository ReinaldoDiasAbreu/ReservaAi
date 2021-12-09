from django.forms import ModelForm, Textarea, NumberInput
from django.utils.translation import gettext_lazy as _
from .models import *


class SalaForm(ModelForm):

    class Meta:
        fields = ['nome', 'descricao', 'capacidade', 'ehPreferencial', 'predio', 'equipamentos']
        model = Sala
        widgets = {
            'capacidade': NumberInput(attrs={'min': 1, 'value': '1'})
        }

class CampusForm(ModelForm):
    class Meta:
        fields = ['nome', 'cnpj', 'telefone', 'horaInicio', 'horaFim', 'logradouro','numero',
                  'bairro','cidade','estado','cep']
        model = Campus
