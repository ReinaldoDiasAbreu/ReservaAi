from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),

    path("users/coordenadorescurso", views.view_coordenadoresCurso, name="coordenadorescurso"),
    path("users/view_coordenadorcurso/<int:id_coordenadorcurso>", views.ver_coordenadorCurso, name="view_coordenadorcurso"),
    path("users/delete_coordenadorcurso/<int:id_coordenadorcurso>", views.delete_coordenadorCurso, name="delete_coordenadorcurso"),

    path("users/professores", views.view_professores, name="professores"),
    path("users/view_professor/<int:id_professor>", views.ver_professor, name="view_professor"),
    path("users/delete_professor/<int:id_professor>", views.delete_professor, name="delete_professor"),
]
