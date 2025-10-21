from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from .models import Fornecedor


class FornecedorForm(forms.ModelForm):
    """Form for Fornecedor model"""
    
    class Meta:
        model = Fornecedor
        fields = [
            'nome', 'cnpj', 'email', 'telefone', 'celular',
            'cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'data-mask': '00.000.000/0000-00'}),
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


class FornecedorSearchForm(forms.Form):
    """Search form for suppliers"""
    search = forms.CharField(
        label='Buscar',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome, CNPJ ou E-mail...'
        })
    )
