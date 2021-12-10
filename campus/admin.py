from django.contrib import admin

from .models import Campus
from .models import Predio
from .models import Equipamento
from .models import Sala


# Adicionando percistência dos models para ser gerenciada no admin
admin.site.register(Campus)
admin.site.register(Predio)
admin.site.register(Equipamento)
admin.site.register(Sala)
