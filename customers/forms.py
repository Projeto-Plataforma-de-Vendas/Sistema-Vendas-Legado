from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Button
from .models import Cliente


class ClienteForm(forms.ModelForm):
    """Form for Cliente model"""
    
    class Meta:
        model = Cliente
        fields = [
            'nome', 'rg', 'cpf', 'email', 'telefone', 'celular',
            'cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'rg': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'data-mask': '000.000.000-00'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'data-mask': '(00) 0000-0000'}),
            'celular': forms.TextInput(attrs={'class': 'form-control', 'data-mask': '(00) 00000-0000'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'id': 'cep', 'data-mask': '00000-000'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'id': 'endereco'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'id': 'bairro'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'id': 'cidade'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'id': 'estado', 'maxlength': '2'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('nome', css_class='col-md-8'),
                Column('cpf', css_class='col-md-4'),
            ),
            Row(
                Column('rg', css_class='col-md-6'),
                Column('email', css_class='col-md-6'),
            ),
            Row(
                Column('telefone', css_class='col-md-6'),
                Column('celular', css_class='col-md-6'),
            ),
            Row(
                Column('cep', css_class='col-md-3'),
                Column('endereco', css_class='col-md-6'),
                Column('numero', css_class='col-md-3'),
            ),
            Row(
                Column('complemento', css_class='col-md-4'),
                Column('bairro', css_class='col-md-4'),
                Column('cidade', css_class='col-md-4'),
            ),
            Row(
                Column('estado', css_class='col-md-2'),
            ),
        )


class ClienteSearchForm(forms.Form):
    """Search form for customers"""
    search = forms.CharField(
        label='Buscar',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome, CPF ou E-mail...'
        })
    )
