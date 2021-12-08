from django.shortcuts import render
from .models import *
from .forms import *


def view_salas(request):
    try:
        if request.user.tipo_usuario == 'CoordenadorEnsino':
            data = {}
            data['form'] = SalaForm(None)
            data['predios'] = Predio.objects.all()

            # Pegando prédio selecionado e filtrando as salas
            predio = request.GET.get('predioselect', -1)
            if predio == -1:
                data['predio'] = data['predios'][0]
                data['predio_nome'] = data['predios'][0].nome
                data['salas'] = Sala.objects.filter(predio=data['predios'][0].id)
            else:
                if len(data['predios']) > 0:
                    data['predio'] = data['predios'][int(predio)-1]
                    data['predio_nome'] = data['predios'][int(predio)-1].nome
                    data['salas'] = Sala.objects.filter(predio=predio)

            # Verificando formulário de salas e salvando
            if request.POST.get('nome', False):
                form = SalaForm(request.POST or None)
                if form.is_valid():
                    form.save()
                    data = {'mensagem': "Sala adicionada com sucesso!" }
                    return render(request, 'campus/salas/cadastro_sucesso.html', data)

            data['form'] = SalaForm(None)
            return render(request, 'campus/salas/salas.html', data)
        else:
            return render(request, 'campus/salas/permission_error.html')
    except:
        data = {'mensagem': "Ocorreu um erro interno!" }
        return render(request, 'campus/salas/error.html', data)


# Faltam as verificações quanto as reservas
def delete_salas(request, id_sala, id_predio):
    try:
        if request.user.tipo_usuario == 'CoordenadorEnsino':
            data = {'mensagem': "Sala " + str(id_sala) + " removida com sucesso!"}
            predio = Predio.objects.get(id=id_predio)
            predio.sala_set.get(pk=id_sala).delete()
            return render(request, 'campus/salas/cadastro_sucesso.html', data)
        else:
            return render(request, 'campus/salas/permission_error.html')
    except:
        data = {'mensagem': "Não foi possível excluir a sala!"}
        return render(request, 'campus/salas/error.html', data)


# Faltam as verificações quanto as reservas
def update_salas(request, id_sala, id_predio):
    try:
        if request.user.tipo_usuario == 'CoordenadorEnsino':
            data = {}
            data['predios'] = Predio.objects.all()

            data['predio'] = Predio.objects.get(id=id_predio)
            data['predio_nome'] = data['predio'].nome
            sala = data['predio'].sala_set.get(id=id_sala)

            data['salas'] = Sala.objects.filter(predio=data['predio'].id)

            form = SalaForm(request.POST or None, instance=sala)
            if form.is_valid():
                sala = form.instance
                sala.predio = data['predio']
                sala.save()
                data = {'mensagem': "Sala atualizada com sucesso!"}
                return render(request, 'campus/salas/cadastro_sucesso.html', data)

            data['form'] = form
            return render(request, 'campus/salas/update_salas.html', data)
        else:
            return render(request, 'campus/salas/permission_error.html')
    except:
        data = {'mensagem': "Não foi possível atualizar a sala!"}
        return render(request, 'campus/salas/error.html', data)


def ver_sala(request, id_sala):
    data = {}
    data['sala'] = Sala.objects.get(id=id_sala)
    if data['sala']:
        return render(request, 'campus/salas/view_sala.html', data)
    else:
        data = {'mensagem': "Não foi possível localizar a sala!"}
        return render(request, 'campus/salas/error.html', data)


