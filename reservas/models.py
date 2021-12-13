from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models
from campus.models import Campus
from users.models import User as UserModel
import datetime


# Validação dos campos


def validate_data(value):
    """Valida se a data da reserva está dentro de um período válido"""
    # Lista de periodos que não venceram
    periodos = Periodo.objects.all()
    periodo_ativo = None
    for periodo in periodos:
        if periodo.dataFim >= datetime.date.today():
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


# Models app Reserva


class Periodo(models.Model):
    dataInicio = models.DateField()
    dataFim = models.DateField()
    coordenadorEnsino = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "[" + str(self.dataInicio) + " até " + str(self.dataFim) + "]"


class Reserva(models.Model):
    titulo = models.CharField(max_length=50)
    descricao = models.CharField(max_length=250, blank=False)
    dataInicio = models.DateField(validators=[validate_data])
    dataFim = models.DateField(validators=[validate_data])
    horaInicio = models.TimeField(validators=[validate_hora])
    horaFim = models.TimeField(validators=[validate_hora])
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)


class OcorrenciaReserva(models.Model):
    data = models.DateField()
    eh_ativa = models.BooleanField(default=True)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)


