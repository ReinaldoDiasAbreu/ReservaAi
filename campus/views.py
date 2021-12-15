from django.shortcuts import render
from datetime import datetime
from reservas.models import Reserva
from .forms import *


def view_salas(request):
    try:
        if not request.user.is_authenticated:
            return render(request, 'permission_error.html')

        if request.user.tipo_usuario == 'CoordenadorEnsino':
            data = {}
            data['form'] = SalaForm(None)
            data['predios'] = Predio.objects.all().order_by('nome')

            # Pegando prédio selecionado e filtrando as salas
            predio = request.GET.get('predioselect', -1)
            if predio == -1 and len(data['predios']) > 0:
                data['predio'] = data['predios'][0]
                data['predio_nome'] = data['predios'][0].nome
                data['salas'] = Sala.objects.filter(predio=data['predios'][0].id)
            else:
                if len(data['predios']) > 0:
                    data['predio'] = Predio.objects.get(id=predio)
                    data['predio_nome'] = data['predio'].nome
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
            return render(request, 'permission_error.html')
    except:
        data = {'mensagem': "Ocorreu um erro interno!" }
        return render(request, 'campus/salas/error.html', data)


def delete_salas(request, id_sala, id_predio):
    try:
        if not request.user.is_authenticated:
            return render(request, 'permission_error.html')

        if request.user.tipo_usuario == 'CoordenadorEnsino':
            predio = Predio.objects.get(id=id_predio)
            sala = predio.sala_set.get(pk=id_sala)
            reservas = Reserva.objects.filter(sala=sala, dataFim__gte=datetime.date.today().strftime("%Y-%m-%d"))
            if len(reservas) > 0:
                data = {'mensagem': "Não foi possível excluir a sala! Há reservas em aberto."}
                return render(request, 'campus/salas/error.html', data)
            else:
                sala.delete()
                data = {'mensagem': "Sala [" + str(sala) + "] removida com sucesso!"}
                return render(request, 'campus/salas/cadastro_sucesso.html', data)
        else:
            return render(request, 'permission_error.html')
    except:
        data = {'mensagem': "Ocorreu um erro interno!"}
        return render(request, 'campus/salas/error.html', data)


def update_salas(request, id_sala, id_predio):
    try:
        if not request.user.is_authenticated:
            return render(request, 'permission_error.html')

        if request.user.tipo_usuario == 'CoordenadorEnsino':
            data = {}
            data['predios'] = Predio.objects.all()

            data['predio'] = Predio.objects.get(id=id_predio)
            data['predio_nome'] = data['predio'].nome
            sala = data['predio'].sala_set.get(id=id_sala)

            data['salas'] = Sala.objects.filter(predio=data['predio'].id)

            form = SalaForm(request.POST or None, instance=sala)
            if form.is_valid():
                reservas = Reserva.objects.filter(sala=sala, dataFim__gte=datetime.date.today().strftime("%Y-%m-%d"))
                if len(reservas) == 0:
                    form.instance.predio = data['predio']
                    form.save()
                    data = {'mensagem': "Sala atualizada com sucesso!"}
                    return render(request, 'campus/salas/cadastro_sucesso.html', data)
                else:
                    data = {'mensagem': "Não foi possível atualizar a sala! Há reservas ativas!"}
                    return render(request, 'campus/salas/error.html', data)

            data['form'] = form
            return render(request, 'campus/salas/update_salas.html', data)
        else:
            return render(request, 'permission_error.html')
    except:
        data = {'mensagem': "Ocorreu um erro interno!"}
        return render(request, 'campus/salas/error.html', data)


def ver_sala(request, id_sala):
    data = {}
    if not request.user.is_authenticated:
        return render(request, 'permission_error.html')
    try:
        sala = Sala.objects.get(id=id_sala)
        if sala:
            data['sala'] = sala
            data['equipamentos'] = sala.equipamentos.all()
            return render(request, 'campus/salas/view_sala.html', data)
        else:
            data = {'mensagem': "Não foi possível localizar a sala!"}
            return render(request, 'campus/salas/error.html', data)
    except:
        data = {'mensagem': "Não foi possível localizar a sala!"}
        return render(request, 'campus/salas/error.html', data)

################# Predios ######################

def view_predios(request):
    try:
        if not request.user.is_authenticated:
            return render(request, 'permission_error.html')

        if request.user.tipo_usuario == 'CoordenadorEnsino':
            data = {}
            data['form'] = PredioForm(None)
            data['campi'] = Campus.objects.all()

            # Pegando campus selecionado e filtrando os prédios
            campus = request.GET.get('campusselect', -1)
            if campus == -1 and len(data['campi']) > 0:
                data['campus'] = data['campi'][0]
                data['campus_nome'] = data['campi'][0].nome
                data['predios'] = Predio.objects.filter(campus=data['campi'][0].id)
            else:
                if len(data['campi']) > 0:
                    data['campus'] = data['campi'][int(campus)-1]
                    data['campus_nome'] = data['campi'][int(campus)-1].nome
                    data['predios'] = Predio.objects.filter(campus=campus)

            # Verificando formulário de prédios e salvando
            if request.POST.get('nome', False):
                form = PredioForm(request.POST or None)
                if form.is_valid():
                    form.save()
                    data = {'mensagem': "Prédio adicionado com sucesso!" }
                    return render(request, 'campus/predios/cadastro_sucesso.html', data)

            data['form'] = PredioForm(None)
            return render(request, 'campus/predios/predios.html', data)
        else:
            return render(request, 'permission_error.html')
    except:
        data = {'mensagem': "Ocorreu um erro interno!" }
        return render(request, 'campus/predios/error.html', data)


def delete_predios(request, id_predio, id_campus):
    try:
        if not request.user.is_authenticated:
            return render(request, 'permission_error.html')

        if request.user.tipo_usuario == 'CoordenadorEnsino':
            campus = Campus.objects.get(id=id_campus)
            predio = campus.predio_set.get(pk=id_predio)
            salas = predio.sala_set.all()
            removed = True
            for sala in salas:
                reservas = Reserva.objects.filter(sala=sala, dataFim__gte=datetime.date.today().strftime("%Y-%m-%d"))
                if len(reservas) > 0:
                    removed = False
                    break

            if removed:
                predio.delete()
                data = {'mensagem': "Predio " + str(id_predio) + " removido com sucesso!"}
                return render(request, 'campus/predios/cadastro_sucesso.html', data)
            else:
                data = {'mensagem': "Não foi possível excluir o prédio! Há salas com reservas pendentes!"}
                return render(request, 'campus/predios/error.html', data)
        else:
            return render(request, 'permission_error.html')
    except:
        data = {'mensagem': "Ocorreu um erro interno!"}
        return render(request, 'campus/predios/error.html', data)


def update_predios(request, id_predio, id_campus):
    try:
        if not request.user.is_authenticated:
            return render(request, 'permission_error.html')

        if request.user.tipo_usuario == 'CoordenadorEnsino':
            data = {}
            data['campi'] = Campus.objects.all()

            data['campus'] = Campus.objects.get(id=id_campus)
            data['campus_nome'] = data['campus'].nome
            predio = data['campus'].predio_set.get(id=id_predio)

            data['predios'] = Predio.objects.filter(campus=data['campus'].id)

            form = PredioForm(request.POST or None, instance=predio)
            if form.is_valid():
                salas = predio.sala_set.all()
                update = True
                for sala in salas:
                    reservas = Reserva.objects.filter(sala=sala, dataFim__gte=datetime.date.today().strftime("%Y-%m-%d"))
                    if len(reservas) > 0:
                        update = False
                        break

                if update:
                    predio = form.instance
                    predio.campus = data['campus']
                    predio.save()
                    data = {'mensagem': "Prédio atualizado com sucesso!"}
                    return render(request, 'campus/predios/cadastro_sucesso.html', data)
                else:
                    data = {'mensagem': "Não foi possível atualizar o prédio! Há salas com reservas pendentes!"}
                    return render(request, 'campus/predios/error.html', data)

            data['form'] = form
            return render(request, 'campus/predios/update_predios.html', data)
        else:
            return render(request, 'permission_error.html')
    except:
        data = {'mensagem': "Não foi possível atualizar o prédio!"}
        return render(request, 'campus/predios/error.html', data)


def ver_predio(request, id_predio):
    data = {}
    if not request.user.is_authenticated:
        return render(request, 'permission_error.html')

    try:
        predio = Predio.objects.get(id=id_predio)
        if predio:
            data['predio'] = predio
            return render(request, 'campus/predios/view_predio.html', data)
        else:
            data = {'mensagem': "Não foi possível localizar o prédio!"}
            return render(request, 'campus/predios/error.html', data)
    except:
        data = {'mensagem': "Não foi possível localizar o prédio!"}
        return render(request, 'campus/predios/error.html', data)


################# Campus ######################

def view_campus(request):
    try:
        if not request.user.is_authenticated:
            return render(request, 'permission_error.html')

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
            return render(request, 'permission_error.html')
    except:
        data = {'mensagem': "Ocorreu um erro interno!" }
        return render(request, 'campus/campus/error.html', data)


def ver_campus(request, id_campus):
    data = {}
    if not request.user.is_authenticated:
        return render(request, 'permission_error.html')
    try:
        campus = Campus.objects.get(id=id_campus)
        if campus:
            data['campus'] = campus
            return render(request, 'campus/campus/view_campus.html', data)
        else:
            data = {'mensagem': "Não foi possível localizar o campus!"}
            return render(request, 'campus/campus/error.html', data)
    except:
        data = {'mensagem': "Não foi possível localizar o campus!"}
        return render(request, 'campus/campus/error.html', data)


def update_campus(request, id_campus):
    try:
        if not request.user.is_authenticated:
            return render(request, 'permission_error.html')

        if request.user.tipo_usuario == 'CoordenadorEnsino':
            data = {}
            data['campi'] = Campus.objects.all()

            data['campus'] = Campus.objects.get(id=id_campus)
            data['campus_nome'] = data['campus'].nome
            campus = Campus.objects.get(id=id_campus)

            form = CampusForm(request.POST or None, instance=campus)
            update = True
            if form.is_valid():
                # Se horário de funcionamento do campus foi alterado
                if form.instance.horaInicio != data['campus'].horaInicio or form.instance.horaFim != data['campus'].horaFim:
                    reservas = Reserva.objects.filter(dataFim__gte=datetime.date.today().strftime("%Y-%m-%d"))
                    print("Horarios diferentes")
                    if len(reservas) > 0:
                        update = False

                if update:
                    campus = form.instance
                    campus.save()
                    data = {'mensagem': "Campus atualizado com sucesso!"}
                    return render(request, 'campus/campus/cadastro_sucesso.html', data)
                else:
                    data = {'mensagem': "Horário de funcionamento não pode ser atualizado, há reservas em aberto!"}
                    return render(request, 'campus/campus/error.html', data)

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
        if not request.user.is_authenticated:
            return render(request, 'permission_error.html')

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
            return render(request, 'permission_error.html')
    except:
        data = {'mensagem': "Ocorreu um erro interno!"}
        return render(request, 'campus/equipamentos/error.html', data)


def ver_equip(request, id_equip):
    data = {}
    if not request.user.is_authenticated:
        return render(request, 'permission_error.html')
    try:
        equip = Equipamento.objects.get(id=id_equip)
        if equip:
            data['equip'] = equip
            return render(request, 'campus/equipamentos/view_equipamento.html', data)
        else:
            data = {'mensagem': "Não foi possível localizar o equipamento!"}
            return render(request, 'campus/equipamentos/error.html', data)
    except:
        data = {'mensagem': "Não foi possível localizar o equipamento!"}
        return render(request, 'campus/equipamentos/error.html', data)


def update_equip(request, id_equip):
    try:
        if not request.user.is_authenticated:
            return render(request, 'permission_error.html')

        if request.user.tipo_usuario == 'CoordenadorEnsino':
            data = {}
            data['equipamentos'] = Equipamento.objects.all()
            data['campus'] = Campus.objects.all()[0]
            data['equipamento'] = Equipamento.objects.get(id=id_equip)
            form = EquipForm(request.POST or None, instance=data['equipamento'])

            if form.is_valid():
                salas = data['equipamento'].sala_set.all()
                if len(salas) == 0:
                    form.save()
                    data = {'mensagem': "Equipamento atualizado com sucesso!"}
                    return render(request, 'campus/equipamentos/cadastro_sucesso.html', data)
                else:
                    data = {'mensagem': "Não foi possível atualizar o equipamento presente em salas!"}
                    return render(request, 'campus/equipamentos/error.html', data)

            data['form'] = form
            return render(request, 'campus/equipamentos/update_equipamento.html', data)
        else:
            return render(request, 'permission_error.html')
    except:
        data = {'mensagem': "Não foi possível atualizar o equipamento!"}
        return render(request, 'campus/equipamentos/error.html', data)


def delete_equip(request, id_equip):
    try:
        if not request.user.is_authenticated:
            return render(request, 'permission_error.html')

        if request.user.tipo_usuario == 'CoordenadorEnsino':
            equip = Equipamento.objects.get(id=id_equip)
            salas = equip.sala_set.all()
            if len(salas) == 0:
                equip.delete()
                data = {'mensagem': "Equipamento " + str(id_equip) + " removido com sucesso!"}
                return render(request, 'campus/equipamentos/cadastro_sucesso.html', data)
            else:
                data = {'mensagem': "Não foi possível excluir o equipamento presente em salas!"}
                return render(request, 'campus/equipamentos/error.html', data)
        else:
            return render(request, 'permission_error.html')
    except:
        data = {'mensagem': "Não foi possível excluir o equipamento!"}
        return render(request, 'campus/equipamentos/error.html', data)
