from django.shortcuts import render
from .forms import *


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

