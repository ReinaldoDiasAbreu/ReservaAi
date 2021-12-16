from django.views.generic import TemplateView
from django.shortcuts import render
from campus.models import Campus
from reservas.models import Reserva
from datetime import datetime
from .models import *
from .forms import *


def view_coordenadoresCurso(request):
    try:
        if not request.user.is_authenticated:
            return render(request, 'permission_error.html')

        if request.user.tipo_usuario == 'CoordenadorEnsino':
            data = {}
            form = UserCreationForm(request.POST or None)
            form.fields['email'].required = True
            form.fields['first_name'].required = True
            form.fields['last_name'].required = True
            campus = Campus.objects.all()
            if len(campus) > 0:
                data['campus'] = campus[0]

            data['coordenadorescurso'] = User.objects.filter(tipo_usuario="CoordenadorCurso")

            if form.is_valid():
                form.instance.tipo_usuario = 'CoordenadorCurso'
                form.save()
                data = {'mensagem': "Coordenador de Curso adicionado com sucesso!" }
                return render(request, 'users/coordenadorEnsino/cadastro_sucesso.html', data)

            data['form'] = form
            return render(request, 'users/coordenadorEnsino/coordenadorescurso.html', data)
        else:
            return render(request, '../../templates/permission_error.html')
    except:
        data = {'mensagem': "Ocorreu um erro interno!" }
        return render(request, 'users/coordenadorEnsino/error.html', data)


def ver_coordenadorCurso(request, id_coordenadorcurso):
    try:
        if not request.user.is_authenticated:
            return render(request, 'permission_error.html')

        if request.user.tipo_usuario == 'CoordenadorEnsino':
            data = {}
            coordenadorCurso = User.objects.get(id=id_coordenadorcurso)
            if coordenadorCurso:
                data['coordenadorcurso'] = coordenadorCurso
                return render(request, 'users/coordenadorEnsino/view_coordenadorcurso.html', data)
            else:
                data = {'mensagem': "Não foi possível localizar o Coordenador de Curso!"}
                return render(request, 'users/coordenadorEnsino/error.html', data)
        else:
            return render(request, 'permission_error.html')
    except:
        data = {'mensagem': "Não foi possível visualizar o coordenador de curso!"}
        return render(request, 'users/coordenadorEnsino/error.html', data)


def delete_coordenadorCurso(request, id_coordenadorcurso):
    try:
        if not request.user.is_authenticated:
            return render(request, 'permission_error.html')

        if request.user.tipo_usuario == 'CoordenadorEnsino':
            data = {'mensagem': "Coordenador de Curso " + str(id_coordenadorcurso) + " removido com sucesso!"}
            coordenadorCurso = User.objects.get(id=id_coordenadorcurso)
            reservas = Reserva.objects.filter(user=coordenadorCurso, dataFim__gte=datetime.today().strftime("%Y-%m-%d"))

            if len(reservas) == 0:
                coordenadorCurso.delete()
                return render(request, 'users/coordenadorEnsino/cadastro_sucesso.html', data)
            else:
                data = {'mensagem': "Não foi possível excluir o Coordenador de Curso! Ele possui reservas em aberto."}
                return render(request, 'users/coordenadorEnsino/error.html', data)
        else:
            return render(request, 'permission_error.html')
    except:
        data = {'mensagem': "Não foi possível excluir o Coordenador de Curso!"}
        return render(request, 'users/coordenadorEnsino/error.html', data)


def view_professores(request):
    try:
        if not request.user.is_authenticated:
            return render(request, 'permission_error.html')

        if request.user.tipo_usuario == 'CoordenadorCurso':
            data = {}
            form = UserCreationForm(request.POST or None)
            form.fields['email'].required = True
            form.fields['first_name'].required = True
            form.fields['last_name'].required = True
            campus = Campus.objects.all()
            if len(campus) > 0:
                data['campus'] = campus[0]

            data['professores'] = User.objects.filter(tipo_usuario="Professor")

            if form.is_valid():
                form.instance.tipo_usuario = 'Professor'
                form.save()
                data = {'mensagem': "Professor adicionado com sucesso!" }
                return render(request, 'users/coordenadorCurso/cadastro_sucesso.html', data)

            data['form'] = form
            return render(request, 'users/coordenadorCurso/professores.html', data)
        else:
            return render(request, 'permission_error.html')
    except:
        data = {'mensagem': "Ocorreu um erro interno!" }
        return render(request, 'users/coordenadorCurso/error.html', data)


def ver_professor(request, id_professor):
    try:
        if not request.user.is_authenticated:
            return render(request, 'permission_error.html')

        if request.user.tipo_usuario == 'CoordenadorCurso':
            data = {}
            professor = User.objects.get(id=id_professor)
            if professor:
                data['professor'] = professor
                return render(request, 'users/coordenadorCurso/view_professor.html', data)
            else:
                data = {'mensagem': "Não foi possível localizar o Professor!"}
                return render(request, 'users/coordenadorCurso/error.html', data)
        else:
            return render(request, 'permission_error.html')
    except:
        data = {'mensagem': "Não foi possível visualizar o Professor!"}
        return render(request, 'users/coordenadorCurso/error.html', data)


def delete_professor(request, id_professor):
    try:
        if not request.user.is_authenticated:
            return render(request, 'permission_error.html')

        if request.user.tipo_usuario == 'CoordenadorCurso':
            professor = User.objects.get(id=id_professor)
            reservas = Reserva.objects.filter(user=professor, dataFim__gte=datetime.today().strftime("%Y-%m-%d"))
            if len(reservas) == 0:
                data = {'mensagem': "Professor removido com sucesso!"}
                professor.delete()
                return render(request, 'users/coordenadorCurso/cadastro_sucesso.html', data)
            else:
                data = {'mensagem': "Não foi possível excluir o Professor! Há reservas em aberto."}
                return render(request, 'users/coordenadorCurso/error.html', data)
        else:
            return render(request, 'permission_error.html')
    except:
        data = {'mensagem': "Ocorreu um erro interno!"}
        return render(request, 'users/coordenadorCurso/error.html', data)
