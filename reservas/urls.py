from django.urls import path
from . import views

app_name = "reservas"

urlpatterns = [
    path("reservas/reservas", views.view_reservas, name="reserva"),
]
