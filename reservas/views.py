from django.shortcuts import render
import pandas as pd
from campus.models import Predio
from .forms import *
from datetime import datetime


def view_reservas(request):
    try:
        data = {}
        if request.user.is_authenticated:
            data['form'] = ReservaForm(None)
            return render(request, 'reservas/reserva.html', data)
        else:
            return render(request, 'users/coordenadorCurso/permission_error.html')
    except:
        data = {'mensagem': "Ocorreu um erro interno!"}
        return render(request, 'users/coordenadorCurso/error.html', data)


def view_all_reservas(request):
    data = {}
    predio_busca = request.GET.get('predio_busca', -1)
    data_busca = request.GET.get('data_busca', -1)

    if predio_busca != -1 and data_busca != -1:
        predio_select = Predio.objects.get(id=predio_busca)
        ocorrencias = OcorrenciaReserva.objects.filter(data=data_busca)
    else:
        predio_select = Predio.objects.all().order_by('nome')[0]
        ocorrencias = OcorrenciaReserva.objects.filter(data=datetime.today())
        data_busca = datetime.today().strftime("%d/%m/%Y")
    data['predio_select'] = predio_select
    data['data_busca'] = data_busca
    if len(ocorrencias) > 0:
        campus = Campus.objects.all()[0]
        if campus:
            fmt = "%H:%M"
            h_ini = campus.horaInicio.strftime(fmt)
            h_fim = campus.horaFim.strftime(fmt)
            hora_inicial = datetime.strptime(h_ini, fmt)
            hora_final = datetime.strptime(h_fim, fmt)
            horarios = pd.date_range(hora_inicial, hora_final, freq="25min").time

            data['horarios'] = horarios
            data['salas'] = Sala.objects.all()
            data['ocorrencias'] = ocorrencias

            reservas_salas = []
            
            data['reservas_salas'] = reservas_salas
        else:
            data['mensagem'] = "Não há campus cadastrado!"
    else:
        data['mensagem'] = "Não existem reservas em nenhuma sala na data pesquisada!"

    predios = Predio.objects.all().order_by('nome')
    data['predios'] = predios
    return render(request, 'reservas/search_reservas.html', data)
