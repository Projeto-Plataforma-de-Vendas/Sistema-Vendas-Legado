from django import forms
from crispy_forms.helper import FormHelper
from .models import Funcionario


class FuncionarioForm(forms.ModelForm):
    """Form for Funcionario model"""
    
    class Meta:
        model = Funcionario
        fields = [
            'nome', 'rg', 'cpf', 'email', 'cargo', 'nivel_acesso',
            'telefone', 'celular', 'cep', 'endereco', 'numero',
            'complemento', 'bairro', 'cidade', 'estado'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'rg': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'data-mask': '000.000.000-00'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'cargo': forms.TextInput(attrs={'class': 'form-control'}),
            'nivel_acesso': forms.Select(
                choices=[
                    ('Administrador', 'Administrador'),
                    ('Usuario', 'Usuário'),
                ],
                attrs={'class': 'form-select'}
            ),
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


class FuncionarioSearchForm(forms.Form):
    """Search form for employees"""
    search = forms.CharField(
        label='Buscar',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome, CPF ou E-mail...'
        })
    )
