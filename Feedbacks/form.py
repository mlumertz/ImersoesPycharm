# -*- coding: UTF-8 -*

from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.forms import BaseInlineFormSet
from datetime import datetime
from Feedbacks.models import *
from django.forms import inlineformset_factory

from functools import partial

DateInput = partial(forms.DateInput, {'class': 'form-control datepicker', 'placeholder': "dd/mm/aaaa"})

Pergunta1_pre = u" Quais são as principais qualidades (forças) de %s?"
Pergunta2_pre = u"Quais são as principais oportunidades de melhorias (fraquezas) de %s?"


Pergunta1_pos = u"Quais são as principais forças que %s tem demonstrado no último ano? Existem algumas cenas que" \
                u" possam exemplificar os argumentos?"
Pergunta2_pos = u"Quais são as principais oportunidades de desenvolvimento para %s ? Existem algumas cenas que possam" \
                u" exemplificar os argumentos?"


class ClienteForm(ModelForm):

    Nome = forms.CharField(max_length=60, label="",
                           widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Nome e Sobrenome", 'id': 'nome'}), )
    Email = forms.EmailField(label="",
                             widget=forms.EmailInput(attrs={'class': "form-control", 'placeholder': "E-mail"}), )

    Deadline = forms.DateField(widget=DateInput(), label="")

    TipoDeFeedback = forms.ChoiceField(label="",
                                       widget=forms.Select( attrs = {'class': "form-control", 'id':'tipoFeedback'}),
                                       choices=Cliente.FEEDBACK_CHOICES)

    FeedbackNome = forms.ChoiceField(label="",
                                       widget=forms.Select( attrs = {'class': "form-control", 'id':'nomeFeedback'}),
                                       choices=Cliente.FEEDBACK_NAME)

    Pergunta1 = forms.CharField(max_length=300, label="", required=False,
                           widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Digite sua pergunta customizada"}), )

    Pergunta2 = forms.CharField(max_length=300, label="", required=False,
                           widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Digite sua pergunta customizada"}), )
    class Meta:
        model = Cliente
        fields = ['Nome', 'Email', 'TipoDeFeedback', 'Deadline', 'FeedbackNome', 'Pergunta1', 'Pergunta2']

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ClienteForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        cliente = super(ClienteForm, self).save(commit=False)

        cliente.Orientador = self.user

        value = cliente.TipoDeFeedback

        if value == Cliente.fb1:

            pergunta1= Pergunta1_pre % (cliente.Nome)
            pergunta2= Pergunta2_pre % (cliente.Nome)
            cliente.Pergunta1 = pergunta1
            cliente.Pergunta2 = pergunta2
        elif value == Cliente.fb2:
            pergunta1= Pergunta1_pos % (cliente.Nome)
            pergunta2= Pergunta2_pos % (cliente.Nome)
            cliente.Pergunta1 = pergunta1
            cliente.Pergunta2 = pergunta2


        if commit:
            cliente.save()

        return cliente

class EditClienteForm(ModelForm):


    Email = forms.EmailField(label="",
                             widget=forms.EmailInput(attrs={'class': "form-control", 'placeholder': "E-mail"}), )

    Deadline = forms.DateField(widget=DateInput(), label="")


    FeedbackNome = forms.ChoiceField(label="",
                                       widget=forms.Select( attrs = {'class': "form-control", 'id':'nomeFeedback'}),
                                       choices=Cliente.FEEDBACK_NAME)

    class Meta:
        model = Cliente
        fields = ['Email', 'Deadline', 'FeedbackNome', ]




class ResponsavelForm(ModelForm):

    Nome = forms.CharField(max_length=100, label="",
                           widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Nome e Sobrenome"}), )

    Id_number = forms.CharField(max_length=10, label="",
                           widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "CRP / CRM "}), )

    Tipo_id = forms.ChoiceField(label = "",
                                widget=forms.Select(attrs={'class': "form-control", }),
                                choices=Responsavel.CATEGORIAS_CHOICES)

    class Meta:
        model = Responsavel
        fields = ['Nome', 'Id_number', 'Tipo_id']



class IndicadoForm(ModelForm):

    Nome = forms.CharField(max_length=60, label="",
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
        self.empty_permitted = False




class IndicadoPageForm(ModelForm):

    Resposta1 = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control"}))

    Resposta2 = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control"}))

    class Meta:
        model = Indicado
        fields = ['Resposta1', 'Resposta2']

class CategoriaInputForm(ModelForm):

    cat = forms.CharField(max_length=50, label="",
                           widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Nova Categoria"}), required=False)

    class Meta:
        model = Categoria
        fields = ['cat']



