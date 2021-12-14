from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models
from campus.models import Campus, Sala
from users.models import User as UserModel
from django import forms
import datetime


# Validação dos campos

def validate_data(value):
    """Valida se a data da reserva está dentro de um período válido"""
    # Lista de periodos que não venceram
    periodos = Periodo.objects.all()
    periodo_ativo = None
    for periodo in periodos:
        if (periodo.dataInicio <= datetime.date.today()) and (periodo.dataFim >= datetime.date.today()) :
            periodo_ativo = periodo
            break

    if periodo_ativo is not None:
        if not (periodo_ativo.dataInicio <= value <= periodo_ativo.dataFim):
            raise ValidationError(
                _('A data não está contida no período atual! ' + str(periodo_ativo))
            )
    else:
        raise ValidationError(
            _('Não existe período de funcionamento válido!')
        )


def validate_hora(value):
    """Valida se a hora inicial da reserva está dentro do horário de funcionamento do campus"""
    # Lista de campus
    campus = Campus.objects.all()
    if len(campus) > 0:
        campus = campus[0]
        if not (campus.horaInicio <= value <= campus.horaFim):
            raise ValidationError(
                _('A hora não está contida no horario de funcionamento do campus! [' +
                  str(campus.horaInicio) + ' até ' + str(campus.horaFim) + ']')
            )
    else:
        raise ValidationError(
            _('Não existe campus cadastrado!')
        )


def validate_periodo(value):
    """Valida se já tem um período ativo"""
    # Lista de periodos que não venceram
    periodos = Periodo.objects.all()
    for periodo in periodos:
        if periodo.dataInicio <= value <= periodo.dataFim:
            raise ValidationError(
                _('Esta data não pode ser usada, já se encontra um período nela! ' + str(periodo))
            )


# Models app Reserva


class Periodo(models.Model):
    dataInicio = models.DateField('Data Inicio')
    dataFim = models.DateField('Data Fim')
    coordenadorEnsino = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "[" + str(self.dataInicio) + " até " + str(self.dataFim) + "]"

    def clean(self):
        periodos = Periodo.objects.all()
        for periodo in periodos:
            if periodo.pk != self.pk:
                if periodo.dataInicio <= datetime.date.today() <= periodo.dataFim:
                    raise ValidationError(
                        _('Esta data não pode ser usada, já se encontra um período nela! ' + str(periodo))
                    )

        if self.dataInicio > self.dataFim:
            raise forms.ValidationError(
                _('A data de fim é anterior a data de início!')
            )


class Reserva(models.Model):
    titulo = models.CharField(max_length=50)
    descricao = models.CharField(max_length=250, blank=False)
    dataInicio = models.DateField('Data Inicio', validators=[validate_data])
    dataFim = models.DateField('Data Fim', validators=[validate_data])
    horaInicio = models.TimeField('Hora Inicio', validators=[validate_hora])
    horaFim = models.TimeField('Hora Fim', validators=[validate_hora])
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, default=None)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, default=None)


class OcorrenciaReserva(models.Model):
    data = models.DateField()
    eh_ativa = models.BooleanField(default=True)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.data) + ' - ' + self.reserva.titulo


