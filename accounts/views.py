from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Funcionario
from .forms import FuncionarioForm, FuncionarioSearchForm


class FuncionarioListView(LoginRequiredMixin, ListView):
    """List all employees - equivalent to FrmFuncionario.java"""
    model = Funcionario
    template_name = 'accounts/funcionario_list.html'
    context_object_name = 'funcionarios'
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
        context['search_form'] = FuncionarioSearchForm(self.request.GET)
        return context


class FuncionarioCreateView(LoginRequiredMixin, CreateView):
    """Create employee"""
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'accounts/funcionario_form.html'
    success_url = reverse_lazy('accounts:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Funcionário cadastrado com sucesso!')
        return super().form_valid(form)


class FuncionarioUpdateView(LoginRequiredMixin, UpdateView):
    """Update employee"""
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'accounts/funcionario_form.html'
    success_url = reverse_lazy('accounts:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Funcionário atualizado com sucesso!')
        return super().form_valid(form)


class FuncionarioDeleteView(LoginRequiredMixin, DeleteView):
    """Delete employee"""
    model = Funcionario
    template_name = 'accounts/funcionario_confirm_delete.html'
    success_url = reverse_lazy('accounts:list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Funcionário excluído com sucesso!')
        return super().delete(request, *args, **kwargs)
