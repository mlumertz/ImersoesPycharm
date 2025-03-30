# !/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.conf import settings
import uuid
from datetime import datetime


class Responsavel(models.Model):

    ct1 = ''
    ct2= 'CRP'
    ct3 = 'CRM'

    CATEGORIAS_CHOICES = (
        (ct1, ''),
        (ct2, 'CRP'),
        (ct3, 'CRM')
    )

    DjangoUser = models.OneToOneField(User, on_delete=models.CASCADE)
    Nome = models.CharField(max_length=100)
    Id_number = models.CharField(max_length=10)
    Tipo_id = models.CharField(max_length=10, choices=CATEGORIAS_CHOICES)

    def __str__(self):
        return self.Nome


class Cliente(models.Model):
    fb1 = u'Feedback I'
    fb2 = u'Feedback II'
    fb3 = u'Customizado'

    FEEDBACK_CHOICES = (
        (fb1, 'Feedback I'),
        (fb2, 'Feedback II'),
        (fb3, 'Customizado'),
    )

    fn1 = u'Aconselhamento de Carreira'
    fn2 = u'Planejamento de Carreira'
    fn3 = u'Coaching de Carreira'

    FEEDBACK_NAME = (
        (fn1, 'Aconselhamento de Carreira'),
        (fn2, 'Planejamento de Carreira'),
        (fn3, 'Coaching de Carreira'),
    )
    Nome = models.CharField(max_length=100)

    Email = models.EmailField()
    Observacoes = models.TextField()
    WebKey = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    Orientador = models.ForeignKey(User, on_delete=models.CASCADE)
    Status = models.BooleanField(default=False)
    FeedbackNome = models.CharField(max_length=50, choices=FEEDBACK_NAME, default=fb1)
    TipoDeFeedback = models.CharField(max_length=50, choices=FEEDBACK_CHOICES, default=fn1)
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
    Categ = models.ForeignKey(Categoria,on_delete=models.CASCADE)
    Status = models.BooleanField(default=False)
    Resposta1 = models.TextField()
    Resposta2 = models.TextField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return self.Nome

    class Meta:
        verbose_name_plural = 'Indicados'
