from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Cliente
from .forms import ClienteForm, ClienteSearchForm


class ClienteListView(LoginRequiredMixin, ListView):
    """
    List all customers - equivalent to FrmCliente.java listar method
    """
    model = Cliente
    template_name = 'customers/cliente_list.html'
    context_object_name = 'clientes'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        
        if search:
            queryset = queryset.filter(
                Q(nome__icontains=search) |
                Q(cpf__icontains=search) |
                Q(email__icontains=search)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ClienteSearchForm(self.request.GET)
        return context


class ClienteCreateView(LoginRequiredMixin, CreateView):
    """
    Create customer - equivalent to FrmCliente.java btnSalvarActionPerformed
    """
    model = Cliente
    form_class = ClienteForm
    template_name = 'customers/cliente_form.html'
    success_url = reverse_lazy('customers:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Cliente cadastrado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao cadastrar cliente. Verifique os dados.')
        return super().form_invalid(form)


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update customer - equivalent to FrmCliente.java btnEditarActionPerformed
    """
    model = Cliente
    form_class = ClienteForm
    template_name = 'customers/cliente_form.html'
    success_url = reverse_lazy('customers:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Cliente atualizado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao atualizar cliente. Verifique os dados.')
        return super().form_invalid(form)


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete customer - equivalent to FrmCliente.java btnExcluirActionPerformed
    """
    model = Cliente
    template_name = 'customers/cliente_confirm_delete.html'
    success_url = reverse_lazy('customers:list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Cliente excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


class BuscarCepView(LoginRequiredMixin, View):
    """
    Search CEP via webservice - equivalent to WebServiceCep functionality
    """
    def get(self, request):
        from core.utils import buscar_cep
        import json
        from django.http import JsonResponse
        
        cep = request.GET.get('cep', '')
        
        if cep:
            dados = buscar_cep(cep)
            if dados:
                return JsonResponse(dados)
        
        return JsonResponse({'erro': 'CEP não encontrado'}, status=404)
