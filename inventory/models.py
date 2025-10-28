from django.db import models, transaction
from django.db.models import F
from suppliers.models import Fornecedor


class Produto(models.Model):
    """
    Product model - equivalent to model/Produto.java
    Maps to tb_produtos table
    """
    descricao = models.CharField('Descrição', max_length=100)
    preco = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    qtd_estoque = models.IntegerField('Quantidade em Estoque')
    estoque_minimo = models.IntegerField('Estoque Mínimo', default=10)  # NOVO
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.PROTECT,
        verbose_name='Fornecedor',
        related_name='produtos',
        db_column='for_id'
    )
    
    class Meta:
        db_table = 'tb_produtos'
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['descricao']
        indexes = [
            models.Index(fields=['qtd_estoque']),  # NOVO: índice para performance
        ]
    
    def __str__(self):
        return f"{self.descricao} (Estoque: {self.qtd_estoque})"
    
    @property
    def estoque_baixo(self):
        """Check if stock is low (less than or equal to minimum)"""
        return self.qtd_estoque <= self.estoque_minimo
    
    @property
    def estoque_disponivel(self):
        """Check if there is available stock"""
        return self.qtd_estoque > 0
    
    @property
    def valor_total_estoque(self):
        """Calculate total stock value"""
        return self.preco * self.qtd_estoque
    
    @transaction.atomic
    def adicionar_estoque(self, quantidade, observacao=''):
        """
        Add stock quantity with database-level update to avoid race conditions
        """
        if quantidade <= 0:
            raise ValueError('Quantidade deve ser maior que zero')
        
        # Atualização atômica no banco
        Produto.objects.filter(pk=self.pk).update(
            qtd_estoque=F('qtd_estoque') + quantidade
        )
        
        # Recarregar objeto
        self.refresh_from_db()
        
        # Registrar movimentação
        MovimentacaoEstoque.objects.create(
            produto=self,
            tipo='ENTRADA',
            quantidade=quantidade,
            quantidade_anterior=self.qtd_estoque - quantidade,
            quantidade_atual=self.qtd_estoque,
            observacao=observacao
        )
        
        return True
    
    @transaction.atomic
    def remover_estoque(self, quantidade, observacao=''):
        """
        Remove stock quantity with validation and database-level locking
        """
        if quantidade <= 0:
            raise ValueError('Quantidade deve ser maior que zero')
        
        # Bloquear linha para evitar race condition
        produto = Produto.objects.select_for_update().get(pk=self.pk)
        
        if produto.qtd_estoque < quantidade:
            raise ValueError(
                f'Estoque insuficiente para {produto.descricao}. '
                f'Disponível: {produto.qtd_estoque}, Solicitado: {quantidade}'
            )
        
        quantidade_anterior = produto.qtd_estoque
        
        # Atualização atômica
        Produto.objects.filter(pk=self.pk).update(
            qtd_estoque=F('qtd_estoque') - quantidade
        )
        
        # Recarregar objeto
        self.refresh_from_db()
        
        # Registrar movimentação
        MovimentacaoEstoque.objects.create(
            produto=self,
            tipo='SAIDA',
            quantidade=quantidade,
            quantidade_anterior=quantidade_anterior,
            quantidade_atual=self.qtd_estoque,
            observacao=observacao
        )
        
        return True


class MovimentacaoEstoque(models.Model):
    """
    Stock movement tracking model (NEW)
    """
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
        ('AJUSTE', 'Ajuste'),
    ]
    
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        related_name='movimentacoes',
        verbose_name='Produto'
    )
    tipo = models.CharField('Tipo', max_length=10, choices=TIPO_CHOICES)
    quantidade = models.IntegerField('Quantidade')
    quantidade_anterior = models.IntegerField('Quantidade Anterior')
    quantidade_atual = models.IntegerField('Quantidade Atual')
    data_movimentacao = models.DateTimeField('Data', auto_now_add=True)
    observacao = models.TextField('Observação', blank=True)
    usuario = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Usuário'
    )
    
    class Meta:
        db_table = 'tb_movimentacoes_estoque'
        verbose_name = 'Movimentação de Estoque'
        verbose_name_plural = 'Movimentações de Estoque'
        ordering = ['-data_movimentacao']
        indexes = [
            models.Index(fields=['produto', '-data_movimentacao']),
        ]
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.produto.descricao} - {self.quantidade}"