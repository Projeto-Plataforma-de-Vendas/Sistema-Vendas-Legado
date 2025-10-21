from django.contrib import admin
from .models import Funcionario


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ['nome', 'cpf', 'email', 'cargo', 'nivel_acesso', 'cidade']
    list_filter = ['nivel_acesso', 'cargo', 'estado']
    search_fields = ['nome', 'cpf', 'email']
    ordering = ['nome']
