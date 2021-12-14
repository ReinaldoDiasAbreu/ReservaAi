from django.shortcuts import render
from .forms import *
from datetime import datetime
import pandas as pd
from django.utils import timezone
from campus.models import Predio


def view_reservas(request):
    try:
        if request.user.is_authenticated:
            data = {}
            data['reservas'] = Reserva.objects.filter(user=request.user.id)
            form = ReservaForm(request.POST or None)

            periodos = Periodo.objects.all()
            periodo_ativo = None
            for periodo in periodos:
                if periodo.dataFim >= timezone.now().date():
                    periodo_ativo = periodo
                    break

            if form.is_valid():
                if form.instance.dataFim < form.instance.dataInicio:
                    form.add_error('dataFim', 'A data final tem que ser posterior ou igual a data inicial!')

                if form.instance.horaFim <= form.instance.horaInicio:
                    form.add_error('horaFim', 'A hora final tem que ser posterior a hora inicial!')

            if form.is_valid() and periodo_ativo is not None:
                form.instance.sala = Sala.objects.get(pk=request.POST.get('sala', -1))
                reservas = Reserva.objects.filter(sala=form.instance.sala)

                dataInicio = form.instance.dataInicio
                dataFim = form.instance.dataFim
                horaInicio = form.instance.horaInicio
                horaFim = form.instance.horaFim

                for res in reservas:
                    # Check if they overlap
                    if ((dataInicio <= res.dataInicio <= dataFim) or (dataInicio <= res.dataFim <= dataFim) or
                       (res.dataInicio <= dataInicio <= res.dataFim) or (res.dataInicio <= dataFim <= res.dataFim)):
                        # If so, check if the time overlap
                        if ((horaInicio <= res.horaInicio < horaFim) or (horaInicio < res.horaFim <= horaFim) or
                           (res.horaInicio <= horaInicio < res.horaFim) or (res.horaInicio < horaFim <= res.horaFim)):
                            data = {'mensagem': "Não foi possível realizar esta reserva, há conflitos com outra!"}
                            return render(request, 'reservas/error.html', data)

                form.instance.user = request.user
                form.instance.periodo = periodo_ativo

                model = form.save()

                dias_reserva = pd.date_range(model.dataInicio, model.dataFim, freq='d')
                res = Reserva.objects.get(id=model.id)
                for dia in dias_reserva:
                    ocR = OcorrenciaReserva()
                    ocR.data = dia
                    ocR.reserva = res
                    ocR.save()

                data = {'mensagem': "Reserva adicionada com sucesso!"}
                return render(request, 'reservas/cadastro_sucesso.html', data)

            data['form'] = form
            return render(request, 'reservas/reserva.html', data)
        else:
            return render(request,
                          'users/coordenadorCurso/../users/templates/users/coordenadorEnsino/permission_error.html')
    except:
        data = {'mensagem': "Ocorreu um erro interno!"}
        return render(request, 'reservas/error.html', data)


def update_reserva(request, id_reserva):
    try:
        if request.user.is_authenticated:
            data = {}
            data['reservas'] = Reserva.objects.filter(user=request.user.id)
            reserva = Reserva.objects.get(id=id_reserva)
            form = ReservaForm(request.POST or None, instance=reserva)

            periodos = Periodo.objects.all()
            periodo_ativo = None
            for periodo in periodos:
                if periodo.dataFim >= timezone.now().date():
                    periodo_ativo = periodo
                    break

            if form.is_valid():
                if form.instance.dataFim < form.instance.dataInicio:
                    form.add_error('dataFim', 'A data final tem que ser posterior ou igual a data inicial!')

                if form.instance.horaFim <= form.instance.horaInicio:
                    form.add_error('horaFim', 'A hora final tem que ser posterior a hora inicial!')

            if form.is_valid() and periodo_ativo is not None:
                form.instance.sala = Sala.objects.get(pk=request.POST.get('sala', -1))
                reservas = Reserva.objects.filter(sala=form.instance.sala).exclude(id=id_reserva)
                #for r in reservas:
                #   print(r.titulo)

                dataInicio = form.instance.dataInicio
                dataFim = form.instance.dataFim
                horaInicio = form.instance.horaInicio
                horaFim = form.instance.horaFim

                for res in reservas:
                    # Check if they overlap
                    if ((dataInicio <= res.dataInicio <= dataFim) or (dataInicio <= res.dataFim <= dataFim) or
                       (res.dataInicio <= dataInicio <= res.dataFim) or (res.dataInicio <= dataFim <= res.dataFim)):
                        # If so, check if the time overlap
                        if ((horaInicio <= res.horaInicio < horaFim) or (horaInicio < res.horaFim <= horaFim) or
                           (res.horaInicio <= horaInicio < res.horaFim) or (res.horaInicio < horaFim <= res.horaFim)):
                            data = {'mensagem': "Não foi possível atualizar esta reserva, há conflitos com outra!"}
                            return render(request, 'reservas/error.html', data)

                form.instance.user = request.user
                form.instance.periodo = periodo_ativo

                model = form.save()

                res = Reserva.objects.get(id=model.id)
                ocorrencias = OcorrenciaReserva.objects.filter(reserva=res)

                for ocorrencia in ocorrencias:
                    ocorrencia.delete()

                dias_reserva = pd.date_range(model.dataInicio, model.dataFim, freq='d')

                for dia in dias_reserva:
                    ocR = OcorrenciaReserva()
                    ocR.data = dia
                    ocR.reserva = res
                    ocR.save()

                data = {'mensagem': "Reserva atualizada com sucesso!"}
                return render(request, 'reservas/cadastro_sucesso.html', data)

            data['form'] = form
            return render(request, 'reservas/update_reserva.html', data)
        else:
            return render(request,
                          'users/coordenadorCurso/../users/templates/users/coordenadorEnsino/permission_error.html')
    except:
        data = {'mensagem': "Ocorreu um erro interno!"}
        return render(request, 'reservas/error.html', data)


def ver_reserva(request, id_reserva):
    data = {}
    reserva = Reserva.objects.get(id=id_reserva)
    if reserva:
        data['reserva'] = reserva
        return render(request, 'reservas/view_reserva.html', data)
    else:
        data = {'mensagem': "Não foi possível localizar a reserva!"}
        return render(request, 'reservas/equipamentos/error.html', data)


def ver_reserva_all(request, id_reserva):
    reserva = Reserva.objects.get(id=id_reserva)
    if reserva:
        data = {}
        data['reserva'] = reserva
        data['user'] = reserva.user
        return render(request, 'reservas/view_reserva_all.html', data)
    else:
        data = {}
        data = {'mensagem': "Não foi possível localizar a reserva!"}
        return render(request, 'reservas/equipamentos/error.html', data)


def view_all_reservas(request):
    data = {}
    data['data_atual'] = datetime.today().strftime("%Y-%m-%d")
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

    data['data_busca'] = data_busca.strftime("%d/%m/%Y")
    predios = Predio.objects.all().order_by('nome')
    data['predios'] = predios
    return render(request, 'reservas/search_reservas.html', data)


def delete_reserva(request, id_reserva):
    try:
        if request.user.is_authenticated:
            data = {'mensagem': "Reserva " + str(id_reserva) + " removida com sucesso!"}
            reserva = Reserva.objects.get(id=id_reserva)
            reserva.delete()
            return render(request, 'reservas/cadastro_sucesso.html', data)
        else:
            return render(request,
                          'users/coordenadorCurso/../users/templates/users/coordenadorEnsino/permission_error.html')
    except:
        data = {'mensagem': "Não foi possível excluir a reserva!"}
        return render(request, 'reservas/error.html', data)
