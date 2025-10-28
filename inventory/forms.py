from django import forms
from django.core.validators import MinValueValidator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from .models import Produto, MovimentacaoEstoque


class ProdutoForm(forms.ModelForm):
    """Form for Produto model"""
    
    class Meta:
        model = Produto
        fields = ['descricao', 'preco', 'qtd_estoque', 'estoque_minimo', 'fornecedor']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'preco': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0.01'}),
            'qtd_estoque': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'estoque_minimo': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'value': '10'}),
            'fornecedor': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean_preco(self):
        preco = self.cleaned_data.get('preco')
        if preco <= 0:
            raise forms.ValidationError('O preço deve ser maior que zero')
        return preco
    
    def clean_qtd_estoque(self):
        qtd = self.cleaned_data.get('qtd_estoque')
        if qtd < 0:
            raise forms.ValidationError('A quantidade não pode ser negativa')
        return qtd
    
    def clean_estoque_minimo(self):
        minimo = self.cleaned_data.get('estoque_minimo')
        if minimo < 1:
            raise forms.ValidationError('O estoque mínimo deve ser pelo menos 1')
        return minimo


class MovimentacaoEstoqueForm(forms.ModelForm):
    """Form for stock movement"""
    
    class Meta:
        model = MovimentacaoEstoque
        fields = ['produto', 'tipo', 'quantidade', 'observacao']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'observacao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')
        if quantidade <= 0:
            raise forms.ValidationError('A quantidade deve ser maior que zero')
        return quantidade


class AjusteEstoqueForm(forms.Form):
    """Form for stock adjustment"""
    produto = forms.ModelChoiceField(
        queryset=Produto.objects.all(),
        label='Produto',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    quantidade_nova = forms.IntegerField(
        label='Nova Quantidade',
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'})
    )
    observacao = forms.CharField(
        label='Motivo do Ajuste',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=True
    )


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
    apenas_estoque_baixo = forms.BooleanField(
        label='Apenas estoque baixo',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
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
        label='Apenas estoque baixo',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    sem_estoque = forms.BooleanField(
        label='Apenas sem estoque',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )