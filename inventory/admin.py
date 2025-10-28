from django.contrib import admin
from .models import Produto, MovimentacaoEstoque


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['descricao', 'preco', 'qtd_estoque', 'estoque_minimo', 'fornecedor', 'estoque_baixo_display', 'valor_estoque_display']
    list_filter = ['fornecedor']
    search_fields = ['descricao', 'fornecedor__nome']
    ordering = ['descricao']
    readonly_fields = ['valor_total_estoque']
    
    def estoque_baixo_display(self, obj):
        return obj.estoque_baixo
    estoque_baixo_display.boolean = True
    estoque_baixo_display.short_description = 'Estoque Baixo'
    
    def valor_estoque_display(self, obj):
        return f'R$ {obj.valor_total_estoque:.2f}'
    valor_estoque_display.short_description = 'Valor Total'


@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = ['data_movimentacao', 'produto', 'tipo', 'quantidade', 'quantidade_anterior', 'quantidade_atual', 'usuario']
    list_filter = ['tipo', 'data_movimentacao']
    search_fields = ['produto__descricao', 'observacao']
    date_hierarchy = 'data_movimentacao'
    readonly_fields = ['data_movimentacao']
    ordering = ['-data_movimentacao']
