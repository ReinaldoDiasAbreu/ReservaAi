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

class EquipForm(ModelForm):
    class Meta:
        fields = ['nome', 'descricao', 'observacao', 'campus']
        model = Equipamento

