from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Produto
from .forms import ProdutoForm, ProdutoSearchForm, EstoqueSearchForm


class ProdutoListView(LoginRequiredMixin, ListView):
    """List all products - equivalent to FrmProduto.java"""
    model = Produto
    template_name = 'inventory/produto_list.html'
    context_object_name = 'produtos'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('fornecedor')
        search = self.request.GET.get('search')
        
        if search:
            queryset = queryset.filter(descricao__icontains=search)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ProdutoSearchForm(self.request.GET)
        return context


class ProdutoCreateView(LoginRequiredMixin, CreateView):
    """Create product"""
    model = Produto
    form_class = ProdutoForm
    template_name = 'inventory/produto_form.html'
    success_url = reverse_lazy('inventory:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Produto cadastrado com sucesso!')
        return super().form_valid(form)


class ProdutoUpdateView(LoginRequiredMixin, UpdateView):
    """Update product"""
    model = Produto
    form_class = ProdutoForm
    template_name = 'inventory/produto_form.html'
    success_url = reverse_lazy('inventory:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Produto atualizado com sucesso!')
        return super().form_valid(form)


class ProdutoDeleteView(LoginRequiredMixin, DeleteView):
    """Delete product"""
    model = Produto
    template_name = 'inventory/produto_confirm_delete.html'
    success_url = reverse_lazy('inventory:list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Produto excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


class EstoqueListView(LoginRequiredMixin, ListView):
    """Stock view - equivalent to FrmEstoque.java"""
    model = Produto
    template_name = 'inventory/estoque_list.html'
    context_object_name = 'produtos'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('fornecedor')
        search = self.request.GET.get('search')
        estoque_baixo = self.request.GET.get('estoque_baixo')
        
        if search:
            queryset = queryset.filter(descricao__icontains=search)
        
        if estoque_baixo:
            queryset = queryset.filter(qtd_estoque__lte=10)
        
        return queryset.order_by('qtd_estoque', 'descricao')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = EstoqueSearchForm(self.request.GET)
        return context
