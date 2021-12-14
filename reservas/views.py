from django.shortcuts import render
from .forms import *
import pandas as pd
from datetime import datetime
from django.utils import timezone


def view_reservas(request):
    #try:
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


        if form.is_valid() and periodo_ativo is not None:
            form.instance.user = request.user
            form.instance.sala = Sala.objects.get(pk=request.POST.get('sala', -1))
            form.instance.periodo = periodo_ativo
            model = form.save()

            fmt = "%Y/%m/%d"

            start_date = datetime.strptime(model.dataInicio.strftime(fmt), fmt)
            end_date = datetime.strptime(model.dataFim.strftime(fmt), fmt)



            dias_reserva = pd.date_range(start_date, end_date, freq='d')
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
        return render(request, 'users/coordenadorCurso/permission_error.html')
    '''except:
        data = {'mensagem': "Ocorreu um erro interno!"}
        return render(request, 'reservas/error.html', data)'''


def ver_reserva(request, id_reserva):
    data = {}
    reserva = Reserva.objects.get(id=id_reserva)
    if reserva:
        data['reserva'] = reserva
        return render(request, 'reservas/view_reserva.html', data)
    else:
        data = {'mensagem': "Não foi possível localizar a reserva!"}
        return render(request, 'reservas/equipamentos/error.html', data)