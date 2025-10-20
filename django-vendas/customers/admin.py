from django.contrib import admin
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'email', 'telefone', 'cidade', 'estado']
    list_filter = ['estado', 'cidade']
    search_fields = ['nome', 'cpf', 'email']
    ordering = ['nome']
