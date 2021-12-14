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
        salas = Sala.objects.all()

        salas_predio = [(i.id, i.nome + " - " + str(i.predio)) for i in salas]
        self.fields['sala'] = forms.ChoiceField(choices=salas_predio)

