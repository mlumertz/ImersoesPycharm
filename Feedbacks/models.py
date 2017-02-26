from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.conf import settings
import uuid
from datetime import datetime

class Cliente(models.Model):
    # fb1 = 'pre'
    # fb2 = 'pos'
    # fb3 = 'cus'
    #
    # FEEDBACK_CHOICES = (
    #     (fb1, 'pré-coaching'),
    #     (fb2, 'pós-coaching'),
    #     (fb3, 'customizado'),
    # )

    Nome = models.CharField(max_length=16)

    Email = models.EmailField()
    Observacoes = models.TextField()
    WebKey = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    Orientador = models.ForeignKey(User)
    Status = models.BooleanField(default=False)
    CRP = models.CharField(max_length=16)
    FeedbackNome = models.CharField(max_length=36)
    TipoDeFeedback = models.CharField(max_length=36)
    Deadline = models.DateField(null=True, blank=True)
    Arquivo = models.FileField()

    def __str__(self):
        return self.Nome

    class Meta:
        verbose_name_plural = 'Clientes'


class Categoria(models.Model):
    cat = models.CharField(max_length=16)
    cliente = models.ForeignKey(Cliente)

    def __str__(self):
        return self.Nome

    class Meta:
        verbose_name_plural = 'Categorias'


class Indicado(models.Model):
    ct1 = 'Amigos'
    ct2 = 'Família'
    ct3 = 'Trabalho'
    ct4 = 'Universidade'

    CATEGORIAS_CHOICES = (
        (ct1, 'Amigos'),
        (ct2, 'Família'),
        (ct3, 'Trabalho'),
        (ct4, 'Universidade'),
    )

    Nome = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    WebKey = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    # Categ = models.CharField( max_length=36, choices= CATEGORIAS_CHOICES, default=ct1)
    Categ = models.CharField(max_length=36)
    Status = models.BooleanField(default=False)
    Resposta1 = models.TextField()
    Resposta2 = models.TextField()
    cliente = models.ForeignKey(Cliente)

    def __str__(self):
        return self.Nome

    class Meta:
        verbose_name_plural = 'Indicados'


