# Generated by Django 3.2.9 on 2021-12-13 13:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Periodo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataInicio', models.DateTimeField()),
                ('dataFim', models.DateTimeField()),
                ('coordenadorEnsino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('descricao', models.CharField(max_length=250)),
                ('dataInicio', models.DateField()),
                ('dataFim', models.DateField()),
                ('horaInicio', models.TimeField()),
                ('horaFim', models.TimeField()),
                ('periodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservas.periodo')),
            ],
        ),
        migrations.CreateModel(
            name='OcorrenciaReserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('eh_ativa', models.BooleanField(default=True)),
                ('reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservas.reserva')),
            ],
        ),
    ]
