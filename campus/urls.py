from django.urls import path
from . import views

app_name = "campus"

urlpatterns = [
    path("campus/view_salas", views.view_salas, name="view_salas"),
]
