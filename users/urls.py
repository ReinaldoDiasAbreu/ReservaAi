from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),

    path("users/coordenadorescurso", views.view_coordenadoresCurso, name="coordenadorescurso"),
    #path("users/new_coordenadorcurso", views.view_coordenadoresCurso, name="new_coordenadorcurso"),
    path("users/view_coordenadorcurso/<int:id_coordenadorcurso>", views.ver_coordenadorCurso, name="view_coordenadorcurso"),
    path("users/delete_coordenadorcurso/<int:id_coordenadorcurso>", views.delete_coordenadorCurso, name="delete_coordenadorcurso"),
    path("users/update_coordenadorcurso/<int:id_coordenadorcurso>", views.update_coordenadorCurso, name="update_coordenadorcurso"),
]
