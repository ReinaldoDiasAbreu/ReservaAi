from django.shortcuts import render


def view_salas(request):
    data = {}
    data['projects'] = Project.objects.all()
    form = ProjectForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('url_home')

    data['form'] = form
    return render(request, 'projects/home.html', data)