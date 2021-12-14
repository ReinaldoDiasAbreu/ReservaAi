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
    predio_busca = request.GET.get('predio_busca', "")
    data_busca = request.GET.get('data_busca', "")

    if predio_busca != "" and data_busca != "":
        predio_select = Predio.objects.get(id=predio_busca)
        data_busca = datetime.strptime(data_busca, '%Y-%m-%d').date()
        ocorrencias = OcorrenciaReserva.objects.filter(data=data_busca, reserva__sala__predio=predio_select)
    else:
        predio_select = Predio.objects.all().order_by('nome')[0]
        ocorrencias = OcorrenciaReserva.objects.filter(data=datetime.today().strftime("%Y-%m-%d"), reserva__sala__predio=predio_select)
        data_busca = datetime.today()
    data['predio_select'] = predio_select

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
            salas = Sala.objects.filter(predio=data['predio_select']).order_by('nome')
            data['salas'] = salas
            data['ocorrencias'] = ocorrencias
            print(len(data['salas']))
            reservas_salas = []
            data_b = data_busca.strftime("%Y-%m-%d")
            for i in range(len(horarios)):
                reservas_salas.append([horarios[i]])
                for j in range(len(salas)):
                    r = Reserva.objects.filter(sala=salas[j], dataInicio__lte=data_b, dataFim__gte=data_b,
                                               horaInicio__lte=horarios[i], horaFim__gte=horarios[i])
                    if len(r) > 0:
                        reservas_salas[i].append(r[0])
                    else:
                        reservas_salas[i].append(False)

            data['reservas_salas'] = reservas_salas
        else:
            data['mensagem'] = "Não há campus cadastrado!"
    else:
        data['mensagem'] = "Não existem reservas em nenhuma sala na data pesquisada!"

    data['data_busca'] = data_busca.strftime("%d-%m-%Y")
    predios = Predio.objects.all().order_by('nome')
    data['predios'] = predios
    return render(request, 'reservas/search_reservas.html', data)
