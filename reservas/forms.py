from django.forms import ModelForm, Textarea, NumberInput, DateInput, TimeInput
from django import forms
from .models import *


class ReservaForm(ModelForm):
    class Meta:
        fields = ['titulo', 'descricao', 'dataInicio', 'dataFim', 'horaInicio',
                  'horaFim']
        model = Reserva
        widgets = {
            'descricao': Textarea(attrs={'rows': '5', 'col': '33'}),
            'dataInicio': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'dataFim': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'horaInicio': TimeInput(attrs={'type': 'time'}),
            'horaFim': TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super(ReservaForm, self).__init__(*args, **kwargs)
        salas = Sala.objects.all().order_by('predio', 'nome')
        salas_predio = [(i.id, str(i.predio) + " - " + i.nome + " - Cap: " + str(i.capacidade) ) for i in salas]
        self.fields['sala'] = forms.ChoiceField(choices=salas_predio)


class PeriodoForm(ModelForm):
    class Meta:
        fields = ['dataInicio', 'dataFim']
        model = Periodo
        widgets = {
            'dataInicio': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'dataFim': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }
