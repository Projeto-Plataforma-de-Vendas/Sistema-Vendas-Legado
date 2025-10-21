from django.contrib import admin
from .models import Venda, ItemVenda


class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra = 1
    fields = ['produto', 'qtd', 'subtotal']
    readonly_fields = ['subtotal']


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'data_venda', 'total_venda']
    list_filter = ['data_venda']
    search_fields = ['cliente__nome']
    date_hierarchy = 'data_venda'
    inlines = [ItemVendaInline]
    readonly_fields = ['total_venda']


@admin.register(ItemVenda)
class ItemVendaAdmin(admin.ModelAdmin):
    list_display = ['venda', 'produto', 'qtd', 'subtotal']
    list_filter = ['venda__data_venda']
    search_fields = ['produto__descricao', 'venda__cliente__nome']
