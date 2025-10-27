from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.db.models import Q, Sum, F, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction

from .models import Produto, MovimentacaoEstoque
from .forms import (
    ProdutoForm, ProdutoSearchForm, EstoqueSearchForm,
    MovimentacaoEstoqueForm, AjusteEstoqueForm
)


class ProdutoListView(LoginRequiredMixin, ListView):
    """List all products - equivalent to FrmProduto.java"""
    model = Produto
    template_name = 'inventory/produto_list.html'
    context_object_name = 'produtos'
    paginate_by = 20
    
    def get_queryset(self):
        # Otimização: select_related para evitar N+1 queries
        queryset = Produto.objects.select_related('fornecedor').annotate(
            valor_estoque=F('preco') * F('qtd_estoque')
        )
        
        search = self.request.GET.get('search', '').strip()
        apenas_estoque_baixo = self.request.GET.get('apenas_estoque_baixo')
        
        if search:
            queryset = queryset.filter(
                Q(descricao__icontains=search) | 
                Q(fornecedor__nome__icontains=search)
            )
        
        if apenas_estoque_baixo:
            queryset = queryset.filter(qtd_estoque__lte=F('estoque_minimo'))
        
        return queryset.order_by('descricao')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = ProdutoSearchForm(self.request.GET)
        
        # Estatísticas
        produtos = Produto.objects.all()
        context['total_produtos'] = produtos.count()
        context['produtos_estoque_baixo'] = produtos.filter(
            qtd_estoque__lte=F('estoque_minimo')
        ).count()
        context['produtos_sem_estoque'] = produtos.filter(qtd_estoque=0).count()
        
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
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao cadastrar produto. Verifique os dados.')
        return super().form_invalid(form)


class ProdutoUpdateView(LoginRequiredMixin, UpdateView):
    """Update product"""
    model = Produto
    form_class = ProdutoForm
    template_name = 'inventory/produto_form.html'
    success_url = reverse_lazy('inventory:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Produto atualizado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao atualizar produto. Verifique os dados.')
        return super().form_invalid(form)


class ProdutoDeleteView(LoginRequiredMixin, DeleteView):
    """Delete product"""
    model = Produto
    template_name = 'inventory/produto_confirm_delete.html'
    success_url = reverse_lazy('inventory:list')
    
    def delete(self, request, *args, **kwargs):
        produto = self.get_object()
        
        # Verificar se há vendas relacionadas
        if produto.itens_venda.exists():
            messages.error(
                request,
                f'Não é possível excluir {produto.descricao} pois existem vendas relacionadas.'
            )
            return redirect('inventory:list')
        
        messages.success(request, f'Produto {produto.descricao} excluído com sucesso!')
        return super().delete(request, *args, **kwargs)


class EstoqueListView(LoginRequiredMixin, ListView):
    """Stock view - equivalent to FrmEstoque.java"""
    model = Produto
    template_name = 'inventory/estoque_list.html'
    context_object_name = 'produtos'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = Produto.objects.select_related('fornecedor').annotate(
            valor_estoque=F('preco') * F('qtd_estoque')
        )
        
        search = self.request.GET.get('search', '').strip()
        estoque_baixo = self.request.GET.get('estoque_baixo')
        sem_estoque = self.request.GET.get('sem_estoque')
        
        if search:
            queryset = queryset.filter(
                Q(descricao__icontains=search) |
                Q(fornecedor__nome__icontains=search)
            )
        
        if estoque_baixo:
            queryset = queryset.filter(qtd_estoque__lte=F('estoque_minimo'))
        
        if sem_estoque:
            queryset = queryset.filter(qtd_estoque=0)
        
        return queryset.order_by('qtd_estoque', 'descricao')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = EstoqueSearchForm(self.request.GET)
        
        # Estatísticas detalhadas
        produtos = Produto.objects.aggregate(
            total_produtos=Count('id'),
            produtos_estoque_baixo=Count('id', filter=Q(qtd_estoque__lte=F('estoque_minimo'))),
            produtos_sem_estoque=Count('id', filter=Q(qtd_estoque=0)),
            valor_total_estoque=Sum(F('preco') * F('qtd_estoque'))
        )
        
        context.update(produtos)
        
        return context


class MovimentacaoEstoqueListView(LoginRequiredMixin, ListView):
    """View stock movements (NEW)"""
    model = MovimentacaoEstoque
    template_name = 'inventory/movimentacao_list.html'
    context_object_name = 'movimentacoes'
    paginate_by = 50
    
    def get_queryset(self):
        queryset = MovimentacaoEstoque.objects.select_related(
            'produto', 'produto__fornecedor', 'usuario'
        )
        
        produto_id = self.request.GET.get('produto')
        tipo = self.request.GET.get('tipo')
        
        if produto_id:
            queryset = queryset.filter(produto_id=produto_id)
        
        if tipo:
            queryset = queryset.filter(tipo=tipo)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['produtos'] = Produto.objects.all().order_by('descricao')
        context['tipos'] = MovimentacaoEstoque.TIPO_CHOICES
        return context


class AjusteEstoqueView(LoginRequiredMixin, View):
    """Manual stock adjustment (NEW)"""
    template_name = 'inventory/ajuste_estoque.html'
    
    def get(self, request):
        form = AjusteEstoqueForm()
        return render(request, self.template_name, {'form': form})
    
    @transaction.atomic
    def post(self, request):
        form = AjusteEstoqueForm(request.POST)
        
        if form.is_valid():
            produto = form.cleaned_data['produto']
            quantidade_nova = form.cleaned_data['quantidade_nova']
            observacao = form.cleaned_data['observacao']
            
            quantidade_anterior = produto.qtd_estoque
            diferenca = quantidade_nova - quantidade_anterior
            
            # Atualizar estoque
            produto.qtd_estoque = quantidade_nova
            produto.save()
            
            # Registrar movimentação
            MovimentacaoEstoque.objects.create(
                produto=produto,
                tipo='AJUSTE',
                quantidade=abs(diferenca),
                quantidade_anterior=quantidade_anterior,
                quantidade_atual=quantidade_nova,
                observacao=f"Ajuste manual: {observacao}",
                usuario=request.user
            )
            
            messages.success(
                request,
                f'Estoque de {produto.descricao} ajustado de {quantidade_anterior} para {quantidade_nova}'
            )
            return redirect('inventory:estoque')
        
        return render(request, self.template_name, {'form': form})