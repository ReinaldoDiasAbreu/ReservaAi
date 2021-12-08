from django.shortcuts import render


def view_salas(request):
    try:
        if request.user.tipo_usuario == 'CoordenadorEnsino':
            return render(request, 'campus/view_salas.html')
        else:
            return render(request, 'campus/permission_error.html')
    except:
        return render(request, 'campus/login_error.html')

