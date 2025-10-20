from django.db import models
from django.contrib.auth.models import User
from customers.models import Cliente
from inventory.models import Produto


class Venda(models.Model):
    """
    Sale model - equivalent to model/Venda.java
    Maps to tb_vendas table
    """
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        verbose_name='Cliente',
        related_name='vendas'
    )
    data_venda = models.DateField('Data da Venda')
    total_venda = models.DecimalField('Total da Venda', max_digits=10, decimal_places=2)
    observacoes = models.TextField('Observações', blank=True)
    
    class Meta:
        db_table = 'tb_vendas'
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
        ordering = ['-data_venda', '-id']
    
    def __str__(self):
        return f'Venda #{self.id} - {self.cliente.nome} - {self.data_venda}'
    
    def calcular_total(self):
        """Calculate total from items"""
        total = sum(item.subtotal for item in self.itens.all())
        self.total_venda = total
        return total


class ItemVenda(models.Model):
    """
    Sale item model - equivalent to model/ItemVenda.java
    Maps to tb_itensvendas table
    """
    venda = models.ForeignKey(
        Venda,
        on_delete=models.CASCADE,
        verbose_name='Venda',
        related_name='itens'
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,
        verbose_name='Produto',
        related_name='itens_venda'
    )
    qtd = models.IntegerField('Quantidade')
    subtotal = models.DecimalField('Subtotal', max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'tb_itensvendas'
        verbose_name = 'Item de Venda'
        verbose_name_plural = 'Itens de Venda'
    
    def __str__(self):
        return f'{self.produto.descricao} - Qtd: {self.qtd}'
    
    def save(self, *args, **kwargs):
        """Calculate subtotal before saving"""
        self.subtotal = self.produto.preco * self.qtd
        super().save(*args, **kwargs)
