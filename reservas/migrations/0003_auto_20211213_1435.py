# Generated by Django 3.2.9 on 2021-12-13 17:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import reservas.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('campus', '0001_initial'),
        ('reservas', '0002_auto_20211213_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='reserva',
            name='sala',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='campus.sala'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='dataFim',
            field=models.DateField(validators=[reservas.models.validate_data]),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='dataInicio',
            field=models.DateField(validators=[reservas.models.validate_data]),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='horaFim',
            field=models.TimeField(validators=[reservas.models.validate_hora]),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='horaInicio',
            field=models.TimeField(validators=[reservas.models.validate_hora]),
        ),
    ]
