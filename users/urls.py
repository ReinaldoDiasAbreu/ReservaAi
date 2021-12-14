from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("users/coordenadorescurso", views.view_coordenadoresCurso, name="coordenadorescurso"),
    path("users/view_coordenadorcurso/<int:id_coordenadorcurso>", views.ver_coordenadorCurso, name="view_coordenadorcurso"),
    path("users/delete_coordenadorcurso/<int:id_coordenadorcurso>", views.delete_coordenadorCurso, name="delete_coordenadorcurso"),
]
