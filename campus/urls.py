from django.urls import path
from . import views

app_name = "campus"

urlpatterns = [
    path("campus/salas", views.view_salas, name="sala"),
    path("campus/new_sala", views.view_salas, name="new_sala"),
    path("campus/view_sala/<int:id_sala>", views.ver_sala, name="view_sala"),
    path("campus/delete_sala/<int:id_sala>/<int:id_predio>", views.delete_salas, name="delete_sala"),
    path("campus/update_sala/<int:id_sala>/<int:id_predio>", views.update_salas, name="update_sala"),
]
