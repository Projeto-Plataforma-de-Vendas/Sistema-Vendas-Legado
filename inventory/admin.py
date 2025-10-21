from django.contrib import admin
from .models import Produto


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'preco', 'qtd_estoque', 'fornecedor', 'estoque_baixo']
    list_filter = ['fornecedor']
    search_fields = ['descricao']
    ordering = ['descricao']
    
    def estoque_baixo(self, obj):
        return obj.estoque_baixo
    estoque_baixo.boolean = True
    estoque_baixo.short_description = 'Estoque Baixo'
