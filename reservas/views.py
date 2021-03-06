from django.shortcuts import render
from .forms import *
from datetime import datetime
import pandas as pd
from django.utils import timezone
from campus.models import Predio
from django.db.models import Q

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
                            data = {'mensagem': "N??o foi poss??vel realizar esta reserva, h?? conflitos com outra!"}
                            return render(request, 'reservas/error.html', data)

                form.instance.user = request.user
                periodo = Periodo.objects.filter(dataInicio__lte=dataInicio.strftime("%Y-%m-%d"),
                                                 dataFim__gte=dataFim.strftime("%Y-%m-%d"))
                print(periodo)
                if len(periodo) > 0:
                    form.instance.periodo = periodo[0]
                    model = form.save()

                    # Criando ocorrencias de reserva
                    dias_reserva = pd.date_range(model.dataInicio, model.dataFim, freq='d')
                    res = Reserva.objects.get(id=model.id)
                    for dia in dias_reserva:
                        ocR = OcorrenciaReserva()
                        ocR.data = dia
                        ocR.reserva = res
                        ocR.save()

                    data = {'mensagem': "Reserva adicionada com sucesso!"}
                    return render(request, 'reservas/cadastro_sucesso.html', data)
                else:
                    data = {'mensagem': "N??o h?? per??odo ativo para a reserva!"}
                    return render(request, 'reservas/error.html', data)

            data['form'] = form
            return render(request, 'reservas/reserva.html', data)
        else:
            return render(request, 'permission_error.html')
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
                            data = {'mensagem': "N??o foi poss??vel atualizar esta reserva, h?? conflitos com outra!"}
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
            return render(request, 'permission_error.html')
    except:
        data = {'mensagem': "Ocorreu um erro interno!"}
        return render(request, 'reservas/error.html', data)


def ver_reserva(request, id_reserva):
    data = {}
    try:
        reserva = Reserva.objects.get(id=id_reserva)
        if reserva:
            data['reserva'] = reserva
            return render(request, 'reservas/view_reserva.html', data)
        else:
            data = {'mensagem': "N??o foi poss??vel localizar a reserva!"}
            return render(request, 'reservas/error.html', data)
    except:
        data = {'mensagem': "N??o foi poss??vel localizar a reserva!"}
        return render(request, 'reservas/error.html', data)


def ver_reserva_all(request, id_reserva):
    try:
        reserva = Reserva.objects.get(id=id_reserva)
        if reserva:
            data = {}
            data['reserva'] = reserva
            data['proprietario'] = reserva.user
            return render(request, 'reservas/view_reserva_all.html', data)
        else:
            data = {}
            data = {'mensagem': "N??o foi poss??vel localizar a reserva!"}
            return render(request, 'reservas/error_all.html', data)
    except:
        data = {}
        data = {'mensagem': "N??o foi poss??vel localizar a reserva!"}
        return render(request, 'reservas/error_all.html', data)


def view_all_reservas(request):

    data = {}
    data['data_atual'] = datetime.today().strftime("%Y-%m-%d")
    predio_busca = request.GET.get('predio_busca', "")
    data_busca = request.GET.get('data_busca', "")
    try:
        if predio_busca != "" and data_busca != "":
            predio_select = Predio.objects.get(id=predio_busca)
            data_busca = datetime.strptime(data_busca, '%Y-%m-%d').date()
            ocorrencias = OcorrenciaReserva.objects.filter(data=data_busca, reserva__sala__predio=predio_select)
        else:
            predio_select = Predio.objects.all().order_by('nome')[0]
            ocorrencias = OcorrenciaReserva.objects.filter(data=datetime.today().strftime("%Y-%m-%d"), reserva__sala__predio=predio_select)
            data_busca = datetime.today()
        data['predio_select'] = predio_select
    except:
        data = {}
        data['mensagem'] = "Houve falha ao buscar pr??dios cadastrados! Contate o coordenador do campus."
        return render(request, 'error_mensage.html', data)

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
                        reservas_salas[i].append(r)
                    else:
                        reservas_salas[i].append(False)

            data['reservas_salas'] = reservas_salas
        else:
            data['mensagem'] = "N??o h?? campus cadastrado!"
    else:
        data['mensagem'] = "N??o existem reservas em nenhuma sala na data pesquisada!"

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
            return render(request, 'permission_error.html')
    except:
        data = {'mensagem': "N??o foi poss??vel excluir a reserva!"}
        return render(request, 'reservas/error.html', data)


def view_periodos(request):
    try:
        if not request.user.is_authenticated:
            return render(request, 'permission_error.html')

        if request.user.tipo_usuario == 'CoordenadorEnsino':
            data = {}
            form = PeriodoForm(request.POST or None)
            data['periodos'] = Periodo.objects.all().order_by('dataInicio')
            data['dataAtual'] = datetime.today().strftime("%Y-%m-%d")

            if form.is_valid():
                form.instance.coordenadorEnsino = request.user
                form.save()
                data = {'mensagem': "Per??odo adicionado com sucesso!"}
                return render(request, 'reservas/periodos/cadastro_sucesso.html', data)

            data['form'] = form
            return render(request, 'reservas/periodos/periodos.html', data)
        else:
            return render(request, 'permission_error.html')
    except:
        data = {'mensagem': "Ocorreu um erro interno!"}
        return render(request, 'reservas/error.html')


def ver_periodo(request, id_periodo):
    try:
        if not request.user.is_authenticated:
            return render(request, 'permission_error.html')

        data = {}
        periodo = Periodo.objects.get(id=id_periodo)
        if periodo:
            data['periodo'] = periodo
            return render(request, 'reservas/periodos/view_periodo.html', data)
        else:
            data = {'mensagem': "N??o foi poss??vel localizar o per??odo!"}
            return render(request, 'reservas/error.html', data)
    except:
        data = {'mensagem': "N??o foi poss??vel localizar o per??odo!"}
        return render(request, 'reservas/error.html', data)


def update_periodo(request, id_periodo):
    try:
        if not request.user.is_authenticated:
            return render(request, 'permission_error.html')

        if request.user.tipo_usuario == 'CoordenadorEnsino':
            data = {}
            data['periodos'] = Periodo.objects.all()
            data['periodo'] = Periodo.objects.get(id=id_periodo)

            form = PeriodoForm(request.POST or None, instance=data['periodo'])
            if form.is_valid():
                reservas = Reserva.objects.filter(periodo=data['periodo'])
                if len(reservas) == 0:
                    form.save()
                    data = {'mensagem': "Per??odo atualizado com sucesso!"}
                    return render(request, 'reservas/periodos/cadastro_sucesso.html', data)
                else:
                    data = {'mensagem': "N??o foi poss??vel atualizar o per??odo! H?? reservas cadastradas."}
                    return render(request, 'reservas/periodos/error.html', data)

            data['form'] = form
            return render(request, 'reservas/periodos/update_periodo.html', data)
        else:
            return render(request, 'permission_error.html')
    except:
        data = {'mensagem': "N??o foi poss??vel atualizar o per??odo!"}
        return render(request, 'reservas/error.html', data)


def delete_periodo(request, id_periodo):
    try:
        if not request.user.is_authenticated:
            return render(request, 'permission_error.html')

        if request.user.tipo_usuario == 'CoordenadorEnsino':
            periodo = Periodo.objects.get(id=id_periodo)
            reservas = Reserva.objects.filter(periodo=periodo)
            if len(reservas) == 0:
                data = {'mensagem': "Per??odo " + str(periodo) + " removido com sucesso!"}
                periodo.delete()
                return render(request, 'reservas/periodos/cadastro_sucesso.html', data)
            else:
                data = {'mensagem': "N??o foi poss??vel excluir o per??odo! Exitem reservas"}
                return render(request, 'reservas/periodos/error.html', data)
        else:
            return render(request, 'permission_error.html')
    except:
        data = {'mensagem': "N??o foi poss??vel excluir o per??odo!"}
        return render(request, 'reservas/periodos/error.html', data)
