# -*- encoding: utf-8 -*-
from django import forms


class UsuarioForm(forms.Form):
    usuario = forms.IntegerField(label='Usuario')


class LibroForm(forms.Form):
    ISBN = forms.IntegerField(label='ISBN Libro')