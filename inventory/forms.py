from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from .models import Produto


class ProdutoForm(forms.ModelForm):
    """Form for Produto model"""
    
    class Meta:
        model = Produto
        fields = ['descricao', 'preco', 'qtd_estoque', 'fornecedor']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'qtd_estoque': forms.NumberInput(attrs={'class': 'form-control'}),
            'fornecedor': forms.Select(attrs={'class': 'form-select'}),
        }


class ProdutoSearchForm(forms.Form):
    """Search form for products"""
    search = forms.CharField(
        label='Buscar',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Descrição do produto...'
        })
    )


class EstoqueSearchForm(forms.Form):
    """Search form for stock view"""
    search = forms.CharField(
        label='Buscar',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Descrição do produto...'
        })
    )
    estoque_baixo = forms.BooleanField(
        label='Apenas estoque baixo (≤ 10)',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
