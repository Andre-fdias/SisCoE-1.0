from django.db import models

class Lembrete(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data = models.DateTimeField()
    tipo = models.CharField(max_length=50, default='Lembrete')
    cor = models.CharField(max_length=7, default='#3788d8')  # Cor padrão azul

    def __str__(self):
        return self.titulo

class Tarefa(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_inicio = models.DateTimeField()
    data_fim = models.DateTimeField()
    tipo = models.CharField(max_length=50, default='Tarefa')
    cor = models.CharField(max_length=7, default='#3788d8')  # Cor padrão azul

    def __str__(self):
        return self.titulo
