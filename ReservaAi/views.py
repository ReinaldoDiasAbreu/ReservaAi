from django.shortcuts import render

def home(request):
    try:
        data = {}
        return render(request, 'ReservaAi/home.html', data)
    except:
        return render(request, 'ReservaAi/erro.html')