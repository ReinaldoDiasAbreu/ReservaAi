from django.db import models


class Campus(models.Model):
    nome = models.CharField(max_length=250)
    cnpj = models.CharField(max_length=20)
    telefone = models.CharField(max_length=15)
    horaInicio = models.TimeField()
    horaFim = models.TimeField()
    logradouro = models.CharField(max_length=250)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=150)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=25)
    cep = models.CharField(max_length=10)


class Predio(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=250)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)


class Equipamento(models.Model):
    nome = models.CharField(max_length=250)
    descricao = models.CharField(max_length=250)
    observacao = models.CharField(max_length=250)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)


class Sala(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=250)
    capacidade = models.IntegerField()
    ehPreferencial = models.BooleanField()
    predio = models.ForeignKey(Predio, on_delete=models.CASCADE)
    equipamentos = models.ManyToManyField(Equipamento)



