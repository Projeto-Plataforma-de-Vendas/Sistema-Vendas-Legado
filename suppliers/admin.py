from django.contrib import admin
from .models import Fornecedor


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cnpj', 'email', 'telefone', 'cidade', 'estado']
    list_filter = ['estado', 'cidade']
    search_fields = ['nome', 'cnpj', 'email']
    ordering = ['nome']
