from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.db.models import Sum, Count
from datetime import datetime, timedelta

from customers.models import Cliente
from suppliers.models import Fornecedor
from inventory.models import Produto
from sales.models import Venda


class LoginView(View):
    """Login view - equivalent to FrmLogin.java"""
    template_name = 'core/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core:dashboard')
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bem-vindo, {user.get_full_name() or user.username}!')
            return redirect('core:dashboard')
        else:
            messages.error(request, 'Usuário ou senha inválidos!')
            return render(request, self.template_name)


class LogoutView(View):
    """Logout view"""
    
    def get(self, request):
        logout(request)
        messages.info(request, 'Você saiu do sistema.')
        return redirect('core:login')


class DashboardView(LoginRequiredMixin, View):
    """Dashboard view - equivalent to FrmMenu.java with statistics"""
    template_name = 'core/dashboard.html'
    
    def get(self, request):
        # Get statistics
        today = datetime.now().date()
        month_start = today.replace(day=1)
        
        # Count records
        total_clientes = Cliente.objects.count()
        total_fornecedores = Fornecedor.objects.count()
        total_produtos = Produto.objects.count()
        total_vendas = Venda.objects.count()
        
        # Sales statistics
        vendas_hoje = Venda.objects.filter(data_venda=today).count()
        vendas_mes = Venda.objects.filter(data_venda__gte=month_start).count()
        
        # Revenue statistics
        total_vendas_valor = Venda.objects.aggregate(
            total=Sum('total_venda')
        )['total'] or 0
        
        vendas_mes_valor = Venda.objects.filter(
            data_venda__gte=month_start
        ).aggregate(total=Sum('total_venda'))['total'] or 0
        
        # Low stock products
        produtos_estoque_baixo = Produto.objects.filter(qtd_estoque__lte=10).order_by('qtd_estoque')[:5]
        
        # Recent sales
        vendas_recentes = Venda.objects.select_related('cliente').order_by('-data_venda')[:10]
        
        context = {
            'total_clientes': total_clientes,
            'total_fornecedores': total_fornecedores,
            'total_produtos': total_produtos,
            'total_vendas': total_vendas,
            'vendas_hoje': vendas_hoje,
            'vendas_mes': vendas_mes,
            'total_vendas_valor': total_vendas_valor,
            'vendas_mes_valor': vendas_mes_valor,
            'produtos_estoque_baixo': produtos_estoque_baixo,
            'vendas_recentes': vendas_recentes,
        }
        
        return render(request, self.template_name, context)
