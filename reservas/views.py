from django.shortcuts import render
from .forms import *
import pandas as pd
from django.utils import timezone


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

                for r in reservas:
                    print(r.titulo)

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
