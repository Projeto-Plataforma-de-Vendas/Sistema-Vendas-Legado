from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q

from .models import Funcionario
from .forms import FuncionarioSearchForm, FuncionarioCreateForm, FuncionarioUpdateForm


LIST_URL = reverse_lazy('accounts:list')


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
    form_class = FuncionarioCreateForm
    template_name = 'accounts/funcionario_form.html'
    success_url = LIST_URL
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Funcionário cadastrado com sucesso e credenciais geradas.'
        )
        return response


class FuncionarioUpdateView(LoginRequiredMixin, UpdateView):
    """Update employee"""
    model = Funcionario
    form_class = FuncionarioUpdateForm
    template_name = 'accounts/funcionario_form.html'
    success_url = LIST_URL
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Funcionário atualizado com sucesso!')
        generated_password = getattr(form, 'generated_password', None)
        if generated_password:
            messages.info(
                self.request,
                'Um novo usuário foi criado para este funcionário. '
                f'Senha temporária: {generated_password}'
            )
        return response


class FuncionarioDeleteView(LoginRequiredMixin, DeleteView):
    """Delete employee"""
    model = Funcionario
    template_name = 'accounts/funcionario_confirm_delete.html'
    success_url = LIST_URL
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Funcionário excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


class AccountPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """Allow logged in users to change their password."""

    template_name = 'accounts/password_change_form.html'
    success_url = reverse_lazy('accounts:password_change_done')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field in form.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
        return form

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Senha alterada com sucesso!')
        return response


class AccountPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    """Confirmation page displayed after password change."""

    template_name = 'accounts/password_change_done.html'
