#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms import BaseInlineFormSet
from datetime import datetime
from Feedbacks.models import *
from django.forms import inlineformset_factory

from functools import partial

DateInput = partial(forms.DateInput, {'class': 'form-control datepicker', 'placeholder': "dd/mm/aaaa"})


class ClienteForm(ModelForm):

    Nome = forms.CharField(max_length=36, label="",
                           widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Nome e Sobrenome"}), )
    Email = forms.EmailField(label="",
                             widget=forms.EmailInput(attrs={'class': "form-control", 'placeholder': "E-mail"}), )

    Deadline = forms.DateField(widget=DateInput(), label="")

    TipoDeFeedback = forms.ChoiceField(label="",
                                       widget=forms.Select( attrs = {'class': "form-control", }),
                                       choices=Cliente.FEEDBACK_CHOICES)

    FeedbackNome = forms.CharField(max_length=36, label="",
                           widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Nome do Questionario"}), )
    class Meta:
        model = Cliente
        fields = ['Nome', 'Email', 'TipoDeFeedback', 'Deadline', 'FeedbackNome']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ClienteForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        cliente = super(ClienteForm, self).save(commit=False)
        cliente.Orientador = self.user

        if commit:
            cliente.save()
        return cliente



class IndicadoForm(ModelForm):

    Nome = forms.CharField(max_length=36, label="",
                           widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Nome e Sobrenome"}), )

    Email = forms.EmailField(label="",
                             widget=forms.EmailInput(attrs={'class': "form-control", 'placeholder': "E-mail"}), )

    Categ = forms.ModelChoiceField(label='categorias',
                                   widget=forms.Select(attrs = {'class': "form-control",}),
                                   queryset=Categoria.objects.none() )

    class Meta:
        model = Indicado
        fields = ['Nome', 'Email', 'Categ']

    def __init__(self, *args, **kwargs):
        cliente =  kwargs.pop('cliente')
        super(IndicadoForm, self).__init__(*args, **kwargs)
        self.fields['Categ'].queryset = Categoria.objects.filter(cliente=cliente)
        self.fields['Categ'].empty_label = 'Selecionar uma Categoria...'


class IndicadoPageForm(ModelForm):

    Resposta1 = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control"}))

    Resposta2 = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control"}))

    class Meta:
        model = Indicado
        fields = ['Resposta1', 'Resposta2']

class CategoriaInputForm(ModelForm):

    cat = forms.CharField(max_length=16, label="",
                           widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Nova Categoria"}), )
    class Meta:
        model = Categoria
        fields = ['cat']



