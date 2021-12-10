from django.views.generic import TemplateView
from django.shortcuts import render
from campus.models import Campus
from .models import *
from .forms import *


class HomePageView(TemplateView):
    template_name = "home.html"


def view_coordenadoresCurso(request):
    try:
        if request.user.tipo_usuario == 'CoordenadorEnsino':
            data = {}
            form = UserCreationForm(request.POST or None)
            form.fields['email'].required = True
            campus = Campus.objects.all()
            if len(campus) > 0:
                data['campus'] = campus[0]

            data['coordenadorescurso'] = User.objects.filter(tipo_usuario="CoordenadorCurso")

            if form.is_valid():
                form.instance.tipo_usuario = 'CoordenadorCurso'
                form.save()
                data = {'mensagem': "Coordenador de Curso adicionado com sucesso!" }
                return render(request, 'users/coordenadorCurso/cadastro_sucesso.html', data)

            data['form'] = form
            return render(request, 'users/coordenadorCurso/coordenadorescurso.html', data)
        else:
            return render(request, 'users/coordenadorCurso/permission_error.html')
    except:
        data = {'mensagem': "Ocorreu um erro interno!" }
        return render(request, 'users/coordenadorCurso/error.html', data)


def ver_coordenadorCurso(request, id_coordenadorcurso):
    try:
        if request.user.tipo_usuario == 'CoordenadorEnsino':
            data = {}
            coordenadorCurso = User.objects.get(id=id_coordenadorcurso)
            if coordenadorCurso:
                data['coordenadorcurso'] = coordenadorCurso
                return render(request, 'users/coordenadorCurso/view_coordenadorcurso.html', data)
            else:
                data = {'mensagem': "Não foi possível localizar o Coordenador de Curso!"}
                return render(request, 'users/coordenadorCurso/error.html', data)
        else:
            return render(request, 'users/coordenadorCurso/permission_error.html')
    except:
        data = {'mensagem': "Não foi possível visualizar o coordenador de curso!"}
        return render(request, 'users/coordenadorCurso/error.html', data)


def delete_coordenadorCurso(request, id_coordenadorcurso):
    try:
        if request.user.tipo_usuario == 'CoordenadorEnsino':
            data = {'mensagem': "Coordenador de Curso " + str(id_coordenadorcurso) + " removido com sucesso!"}
            coordenadorCurso = User.objects.get(id=id_coordenadorcurso)
            n = coordenadorCurso.delete()
            print("Removidos: ", n)
            return render(request, 'users/coordenadorCurso/cadastro_sucesso.html', data)
        else:
            return render(request, 'users/coordenadorCurso/permission_error.html')
    except:
        data = {'mensagem': "Não foi possível excluir o Coordenador de Curso!"}
        return render(request, 'users/coordenadorCurso/error.html', data)
