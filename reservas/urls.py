from django.urls import path
from . import views

app_name = "reservas"

urlpatterns = [
    path("", views.view_all_reservas, name="view_all_reservas"),
    path("reservas/reservas", views.view_reservas, name="reserva"),
]
