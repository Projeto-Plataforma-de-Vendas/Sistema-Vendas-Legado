from django import forms
from django.forms import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from .models import Venda, ItemVenda
from customers.models import Cliente
from inventory.models import Produto


class VendaForm(forms.ModelForm):
    """Form for Venda model"""
    
    class Meta:
        model = Venda
        fields = ['cliente', 'data_venda', 'observacoes']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'data_venda': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ItemVendaForm(forms.ModelForm):
    """Form for ItemVenda model"""
    
    class Meta:
        model = ItemVenda
        fields = ['produto', 'qtd']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-select'}),
            'qtd': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }
    
    def clean_qtd(self):
        """Validate stock availability"""
        qtd = self.cleaned_data.get('qtd')
        produto = self.cleaned_data.get('produto')
        
        if produto and qtd:
            if qtd > produto.qtd_estoque:
                raise forms.ValidationError(
                    f'Quantidade indisponível. Estoque atual: {produto.qtd_estoque}'
                )
        
        return qtd


# Formset for managing multiple items in a sale
ItemVendaFormSet = inlineformset_factory(
    Venda,
    ItemVenda,
    form=ItemVendaForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)


class VendaSearchForm(forms.Form):
    """Search form for sales"""
    data_inicio = forms.DateField(
        label='Data Início',
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    data_fim = forms.DateField(
        label='Data Fim',
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    cliente = forms.ModelChoiceField(
        label='Cliente',
        queryset=Cliente.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
