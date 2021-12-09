from django.urls import path
from . import views

app_name = "campus"

urlpatterns = [
    path("campus/salas", views.view_salas, name="sala"),
    path("campus/new_sala", views.view_salas, name="new_sala"),
    path("campus/view_sala/<int:id_sala>", views.ver_sala, name="view_sala"),
    path("campus/delete_sala/<int:id_sala>/<int:id_predio>", views.delete_salas, name="delete_sala"),
    path("campus/update_sala/<int:id_sala>/<int:id_predio>", views.update_salas, name="update_sala"),

    path("campus/campus", views.view_campus, name="campus"),
    path("campus/new_campus", views.view_campus, name="new_campus"),
    path("campus/view_campus/<int:id_campus>", views.ver_campus, name="view_campus"),
    path("campus/update_campus/<int:id_campus>", views.update_campus, name="update_campus"),

    path("campus/equipamentos", views.view_equips, name="equipamento"),
    path("campus/new_equip", views.view_equips, name="new_equip"),
    path("campus/view_equip/<int:id_equip>", views.ver_equip, name="view_equip"),
    path("campus/delete_equip/<int:id_equip>", views.delete_equip, name="delete_equip"),
    path("campus/update_equip/<int:id_equip>", views.update_equip, name="update_equip"),

]
