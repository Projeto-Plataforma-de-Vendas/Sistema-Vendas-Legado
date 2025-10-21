from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.db import transaction
from django.db.models import Q, Sum
from datetime import datetime

from .models import Venda, ItemVenda
from .forms import VendaForm, ItemVendaFormSet, VendaSearchForm
from inventory.models import Produto


class VendaListView(LoginRequiredMixin, ListView):
    """List all sales - equivalent to FrmHistorico.java"""
    model = Venda
    template_name = 'sales/venda_list.html'
    context_object_name = 'vendas'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('cliente')
        
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')
        cliente_id = self.request.GET.get('cliente')
        
        if data_inicio:
            queryset = queryset.filter(data_venda__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(data_venda__lte=data_fim)
        if cliente_id:
            queryset = queryset.filter(cliente_id=cliente_id)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = VendaSearchForm(self.request.GET)
        
        # Calculate total
        vendas = self.get_queryset()
        context['total_vendas'] = vendas.aggregate(total=Sum('total_venda'))['total'] or 0
        
        return context


class VendaCreateView(LoginRequiredMixin, View):
    """
    Create sale with items - equivalent to FrmVenda.java
    Handles the complex transaction of creating sale + items + updating stock
    """
    template_name = 'sales/venda_form.html'
    
    def get(self, request):
        form = VendaForm()
        formset = ItemVendaFormSet()
        
        context = {
            'form': form,
            'formset': formset,
            'title': 'Nova Venda',
        }
        return render(request, self.template_name, context)
    
    @transaction.atomic
    def post(self, request):
        form = VendaForm(request.POST)
        formset = ItemVendaFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            # Save sale
            venda = form.save(commit=False)
            venda.total_venda = 0
            venda.save()
            
            # Save items and update stock
            total = 0
            for item_form in formset:
                if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE'):
                    item = item_form.save(commit=False)
                    item.venda = venda
                    
                    # Calculate subtotal
                    item.subtotal = item.produto.preco * item.qtd
                    total += item.subtotal
                    
                    # Update stock
                    produto = item.produto
                    if not produto.remover_estoque(item.qtd):
                        messages.error(
                            request,
                            f'Estoque insuficiente para {produto.descricao}'
                        )
                        transaction.set_rollback(True)
                        context = {
                            'form': form,
                            'formset': formset,
                            'title': 'Nova Venda',
                        }
                        return render(request, self.template_name, context)
                    
                    item.save()
            
            # Update sale total
            venda.total_venda = total
            venda.save()
            
            messages.success(request, f'Venda #{venda.id} cadastrada com sucesso!')
            return redirect('sales:detail', pk=venda.pk)
        
        context = {
            'form': form,
            'formset': formset,
            'title': 'Nova Venda',
        }
        return render(request, self.template_name, context)


class VendaDetailView(LoginRequiredMixin, DetailView):
    """View sale details - equivalent to FrmDetalheVenda.java"""
    model = Venda
    template_name = 'sales/venda_detail.html'
    context_object_name = 'venda'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['itens'] = self.object.itens.select_related('produto')
        return context


class VendaDeleteView(LoginRequiredMixin, DeleteView):
    """Delete sale and restore stock"""
    model = Venda
    template_name = 'sales/venda_confirm_delete.html'
    success_url = reverse_lazy('sales:list')
    
    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        venda = self.get_object()
        
        # Restore stock for all items
        for item in venda.itens.all():
            item.produto.adicionar_estoque(item.qtd)
        
        messages.success(request, f'Venda #{venda.id} excluída com sucesso!')
        return super().delete(request, *args, **kwargs)


class TotalVendaView(LoginRequiredMixin, View):
    """
    View total sales by period - equivalent to FrmTotalVenda.java
    """
    template_name = 'sales/total_venda.html'
    
    def get(self, request):
        form = VendaSearchForm(request.GET)
        vendas = Venda.objects.all()
        
        if form.is_valid():
            data_inicio = form.cleaned_data.get('data_inicio')
            data_fim = form.cleaned_data.get('data_fim')
            
            if data_inicio:
                vendas = vendas.filter(data_venda__gte=data_inicio)
            if data_fim:
                vendas = vendas.filter(data_venda__lte=data_fim)
        
        total = vendas.aggregate(total=Sum('total_venda'))['total'] or 0
        
        context = {
            'form': form,
            'total': total,
            'vendas': vendas.select_related('cliente'),
        }
        return render(request, self.template_name, context)
