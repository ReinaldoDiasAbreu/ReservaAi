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
            if predio == -1 and len(data['predios']) > 0:
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
    sala = Sala.objects.get(id=id_sala)
    if sala:
        data['sala'] = sala
        data['equipamentos'] = sala.equipamentos.all()
        return render(request, 'campus/salas/view_sala.html', data)
    else:
        data = {'mensagem': "Não foi possível localizar a sala!"}
        return render(request, 'campus/salas/error.html', data)


################# Campus ######################

def view_campus(request):
    try:
        if request.user.tipo_usuario == 'CoordenadorEnsino':
            data = {}
            campus = Campus.objects.all()
            if len(campus) > 0:
                data['campus'] = campus[0]
            else:
                data['campus'] = ""

            # Verificando formulário de salas e salvando
            if request.POST.get('nome', False):
                form = CampusForm(request.POST or None)
                if form.is_valid():
                    form.save()
                    data = {'mensagem': "Campus adicionado com sucesso!" }
                    return render(request, 'campus/campus/cadastro_sucesso.html', data)

            data['form'] = CampusForm(None)
            return render(request, 'campus/campus/campus.html', data)
        else:
            return render(request, 'campus/campus/permission_error.html')
    except:
        data = {'mensagem': "Ocorreu um erro interno!" }
        return render(request, 'campus/campus/error.html', data)

def ver_campus(request, id_campus):
    data = {}
    campus = Campus.objects.get(id=id_campus)
    if campus:
        data['campus'] = campus
        return render(request, 'campus/campus/view_campus.html', data)
    else:
        data = {'mensagem': "Não foi possível localizar o campus!"}
        return render(request, 'campus/campus/error.html', data)

def update_campus(request, id_campus):
    try:
        if request.user.tipo_usuario == 'CoordenadorEnsino':
            data = {}
            data['campi'] = Campus.objects.all()

            data['campus'] = Campus.objects.get(id=id_campus)
            data['campus_nome'] = data['campus'].nome
            campus = Campus.objects.get(id=id_campus)

            form = CampusForm(request.POST or None, instance=campus)
            if form.is_valid():
                campus = form.instance
                campus.save()
                data = {'mensagem': "Campus atualizado com sucesso!"}
                return render(request, 'campus/campus/cadastro_sucesso.html', data)

            data['form'] = form
            return render(request, 'campus/campus/update_campus.html', data)
        else:
            return render(request, 'permission_error.html')
    except:
        data = {'mensagem': "Não foi possível atualizar o campus!"}
        return render(request, 'campus/campus/error.html', data)

################# Equipamentos ######################

def view_equips(request):
    try:
        if request.user.tipo_usuario == 'CoordenadorEnsino':
            data = {}
            form = EquipForm(request.POST or None)
            campus = Campus.objects.all()
            if len(campus) > 0:
                data['campus'] = campus[0]
            data['equipamentos'] = Equipamento.objects.all()

            if form.is_valid():
                form.save()
                data = {'mensagem': "Equipamento adicionado com sucesso!" }
                return render(request, 'campus/equipamentos/cadastro_sucesso.html', data)

            data['form'] = form
            return render(request, 'campus/equipamentos/equipamentos.html', data)
        else:
            return render(request, 'campus/equipamentos/permission_error.html')
    except:
        data = {'mensagem': "Ocorreu um erro interno!" }
        return render(request, 'campus/equipamentos/error.html', data)


def ver_equip(request, id_equip):
    data = {}
    equip = Equipamento.objects.get(id=id_equip)
    if equip:
        data['equip'] = equip
        return render(request, 'campus/equipamentos/view_equipamento.html', data)
    else:
        data = {'mensagem': "Não foi possível localizar o equipamento!"}
        return render(request, 'campus/equipamentos/error.html', data)


def update_equip(request, id_equip):
    try:
        if request.user.tipo_usuario == 'CoordenadorEnsino':
            data = {}
            data['equipamentos'] = Equipamento.objects.all()
            data['campus'] = Campus.objects.all()[0]
            data['equipamento'] = Equipamento.objects.get(id=id_equip)
            form = EquipForm(request.POST or None, instance=data['equipamento'])

            if form.is_valid():
                form.save()
                data = {'mensagem': "Equipamento atualizado com sucesso!"}
                return render(request, 'campus/equipamentos/cadastro_sucesso.html', data)

            data['form'] = form
            return render(request, 'campus/equipamentos/update_equipamento.html', data)
        else:
            return render(request, 'campus/equipamentos/permission_error.html')
    except:
        data = {'mensagem': "Não foi possível atualizar o equipamento!"}
        return render(request, 'campus/equipamentos/error.html', data)


def delete_equip(request, id_equip):
    try:
        if request.user.tipo_usuario == 'CoordenadorEnsino':
            data = {'mensagem': "Equipamento " + str(id_equip) + " removido com sucesso!"}
            equip = Equipamento.objects.get(id=id_equip)
            equip.delete()
            return render(request, 'campus/equipamentos/cadastro_sucesso.html', data)
        else:
            return render(request, 'campus/equipamentos/permission_error.html')
    except:
        data = {'mensagem': "Não foi possível excluir o equipamento!"}
        return render(request, 'campus/equipamentos/error.html', data)