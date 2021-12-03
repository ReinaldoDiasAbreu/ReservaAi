from django.shortcuts import render


def home(request):
    try:
        data = {
            'text': "Bem vindo!"
        }
        return render(request, 'ReservaAi/home.html', data)
    except:
        return render(request, 'ReservaAi/erro.html')
