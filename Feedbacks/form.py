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

DateInput = partial(forms.DateInput, {'class': 'form-control datepicker'})


class ClienteForm(ModelForm):
    Nome = forms.CharField(max_length=16, label="",
                           widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Nome"}), )
    Email = forms.EmailField(label="",
                             widget=forms.EmailInput(attrs={'class': "form-control", 'placeholder': "E-mail"}), )
    Deadline = forms.DateField(widget=DateInput(), label="Data Limite:")
    TipoDeFeedback = forms.CharField(label="Tipo de Feedback", widget=forms.Select( attrs = {'class': "dropdown"}), ),

    #attrs = {'class': "dropdown-menu"}
    class Meta:
        model = Cliente
        fields = ['Nome', 'Email', 'TipoDeFeedback', 'Deadline']

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
                                   widget=forms.Select(attrs = {'class': "form-control"}),
                                   queryset=Categoria.objects.none() )

    class Meta:
        model = Indicado
        fields = ['Nome', 'Email', 'Categ']

    def __init__(self, *args, **kwargs):
        cliente =  kwargs.pop('cliente')
        super(IndicadoForm, self).__init__(*args, **kwargs)
        self.fields['Categ'].queryset = Categoria.objects.filter(cliente=cliente)


class IndicadoPageForm(ModelForm):
    class Meta:
        model = Indicado
        fields = ['Resposta1', 'Resposta2']

class CategoriaInputForm(ModelForm):

    cat = forms.CharField(max_length=16, label="",
                           widget=forms.TextInput(attrs={'class': "form-control", 'placeholder': "Nova Categoria"}), )
    class Meta:
        model = Categoria
        fields = ['cat']

#    def get_available_choices(arg):

#
#     listnames = []
#     listCat = Categoria.objects.filter(cliente=arg)
#
#     for item in listCat:
#         listnames.append(item.cat)
#
#     return listnames
#
# class BaseIndicadoFormSet(BaseInlineFormSet):
#     def clean(self):
#         """
#         Adds validation to check that no two links have the same anchor or URL
#         and that all links have both an anchor and URL.
#         """
#         if any(self.errors):
#             return
#
#         nomes = []
#         emails = []
#         duplicates = False
#
#         for form in self.forms:
#             if form.cleaned_data:
#                 nome = form.cleaned_data['Nome']
#                 email = form.cleaned_data['Email']
#
#                 # Check that no two links have the same anchor or URL
#                 if nome and email:
#                     if nome in nomes:
#                         duplicates = True
#                     nomes.append(nome)
#
#                     if email in emails:
#                         duplicates = True
#                     emails.append(nome)
#
#                 if duplicates:
#                     raise forms.ValidationError(
#                         'Indicados devem ter nome e email único',
#                         code='indicados_duplicados'
#                     )
#
#                 # Check that all links have both an anchor and URL
#                 if email and not nome:
#                     raise forms.ValidationError(
#                         'Todos os indicados devem ter um nome associado.',
#                         code='missing_nome'
#                     )
#                 elif nome and not email:
#                     raise forms.ValidationError(
#                         'Todos os indicados devem ter um email associado.',
#                         code='missing_email'
#                     )
#
#
# class BaseCategoriaFormset(BaseInlineFormSet):
#     def add_fields(self, form, index):
#
#         # allow the super class to create the fields as usual
#         super(BaseCategoriaFormset, self).add_fields(form, index)
#
#         form.nested = self.nested_formset_class(
#             instance=form.instance,
#             data=form.data if self.is_bound else None,
#             prefix='%s-%s' % (
#                 form.prefix,
#                 self.nested_formset_class.get_default_prefix(),
#             ),
#         )
#
#     def is_valid(self):
#
#         result = super(BaseCategoriaFormset, self).is_valid()
#
#         if self.is_bound:
#             # look at any nested formsets, as well
#             for form in self.forms:
#                 result = result and form.nested.is_valid()
#
#         return result
#
#     def save(self, commit=True):
#
#         result = super(BaseCategoriaFormset, self).save(commit=commit)
#
#         for form in self:
#             form.nested.save(commit=commit)
#
#         return result
#
#
# def nested_formset_factory(parent_model, child_model, grandchild_model, child_form, grandchild_form, extra):
#     parent_child = inlineformset_factory(
#         parent_model,
#         child_model,
#         form=child_form,
#         formset=BaseCategoriaFormset,
#         extra=extra,
#     )
#
#     parent_child.nested_formset_class = inlineformset_factory(
#         child_model,
#         grandchild_model,
#         form=grandchild_form,
#         extra=extra,
#     )
#
#     return parent_child

