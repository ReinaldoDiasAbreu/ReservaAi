from django.urls import path
from . import views

app_name = "reservas"

urlpatterns = [
    path("", views.view_all_reservas, name="view_all_reservas"),
    path("reservas/view_reserva_all/<int:id_reserva>", views.ver_reserva_all, name="view_reserva_all"),
    path("reservas/reservas", views.view_reservas, name="reserva"),
    path("reservas/view_reserva/<int:id_reserva>", views.ver_reserva, name="view_reserva"),
    path("reservas/delete_reserva/<int:id_reserva>", views.delete_reserva, name="delete_reserva"),
    path("reservas/update_reserva/<int:id_reserva>", views.update_reserva, name="update_reserva"),
]
