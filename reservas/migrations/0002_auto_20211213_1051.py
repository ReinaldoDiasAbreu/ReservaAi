# Generated by Django 3.2.9 on 2021-12-13 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodo',
            name='dataFim',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='periodo',
            name='dataInicio',
            field=models.DateField(),
        ),
    ]
