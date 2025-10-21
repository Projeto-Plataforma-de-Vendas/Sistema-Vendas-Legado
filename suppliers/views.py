from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Fornecedor
from .forms import FornecedorForm, FornecedorSearchForm


class FornecedorListView(LoginRequiredMixin, ListView):
    """List all suppliers - equivalent to FrmFornecedor.java"""
    model = Fornecedor
    template_name = 'suppliers/fornecedor_list.html'
    context_object_name = 'fornecedores'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        
        if search:
            queryset = queryset.filter(
                Q(nome__icontains=search) |
                Q(cnpj__icontains=search) |
                Q(email__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = FornecedorSearchForm(self.request.GET)
        return context


class FornecedorCreateView(LoginRequiredMixin, CreateView):
    """Create supplier"""
    model = Fornecedor
    form_class = FornecedorForm
    template_name = 'suppliers/fornecedor_form.html'
    success_url = reverse_lazy('suppliers:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Fornecedor cadastrado com sucesso!')
        return super().form_valid(form)


class FornecedorUpdateView(LoginRequiredMixin, UpdateView):
    """Update supplier"""
    model = Fornecedor
    form_class = FornecedorForm
    template_name = 'suppliers/fornecedor_form.html'
    success_url = reverse_lazy('suppliers:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Fornecedor atualizado com sucesso!')
        return super().form_valid(form)


class FornecedorDeleteView(LoginRequiredMixin, DeleteView):
    """Delete supplier"""
    model = Fornecedor
    template_name = 'suppliers/fornecedor_confirm_delete.html'
    success_url = reverse_lazy('suppliers:list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Fornecedor excluído com sucesso!')
        return super().delete(request, *args, **kwargs)
