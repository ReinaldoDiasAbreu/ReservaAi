from django.urls import path
from . import views

app_name = "reservas"

urlpatterns = [
    path("reservas/reservas", views.view_reservas, name="reserva"),
    path("reservas/view_reserva/<int:id_reserva>", views.ver_reserva, name="view_reserva"),
]
