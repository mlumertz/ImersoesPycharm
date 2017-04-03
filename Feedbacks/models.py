from __future__ import unicode_literals
# !/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.conf import settings
import uuid
from datetime import datetime


class Responsavel(models.Model):
    DjangoUser = models.OneToOneField(User, on_delete=models.CASCADE)
    Nome = models.CharField(max_length=100)
    CRP = models.CharField(max_length=50)

    def __str__(self):
        return self.Nome

    class Meta:
        verbose_name_plural = 'Responsaveis'


class Cliente(models.Model):
    fb1 = 'Pre-Coaching'
    fb2 = 'Pos-Coaching'
    fb3 = 'Customizado'

    FEEDBACK_CHOICES = (
        (fb1, 'pre-coaching'),
        (fb2, 'pos-coaching'),
        (fb3, 'customizado'),
    )

    Nome = models.CharField(max_length=100)

    Email = models.EmailField()
    Observacoes = models.TextField()
    WebKey = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    Orientador = models.ForeignKey(User)
    Status = models.BooleanField(default=False)
    FeedbackNome = models.CharField(max_length=50)
    TipoDeFeedback = models.CharField(max_length=50, choices=FEEDBACK_CHOICES, default=fb1)
    Deadline = models.DateField(null=True, blank=True)
    StatusDeadline = models.BooleanField(default=False)
    Arquivo = models.FileField()
    ProgressBar = models.DecimalField(default=0, max_digits=3, decimal_places=0)
    Pergunta1 = models.TextField()
    Pergunta2 = models.TextField()

    def __str__(self):
        return self.Nome

    class Meta:
        verbose_name_plural = 'Clientes'


class Categoria(models.Model):
    cat = models.CharField(max_length=50)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return self.Nome

    class Meta:
        verbose_name_plural = 'Categorias'

    def __unicode__(self):
        return self.cat


class Indicado(models.Model):
    ct1 = 'Amigos'
    ct2 = 'Familia'
    ct3 = 'Trabalho'
    ct4 = 'Universidade'

    CATEGORIAS_CHOICES = (
        (ct1, 'Amigos'),
        (ct2, 'Familia'),
        (ct3, 'Trabalho'),
        (ct4, 'Universidade'),
    )

    Nome = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    WebKey = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    Categ = models.ForeignKey(Categoria)
    Status = models.BooleanField(default=False)
    Resposta1 = models.TextField()
    Resposta2 = models.TextField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return self.Nome

    class Meta:
        verbose_name_plural = 'Indicados'
