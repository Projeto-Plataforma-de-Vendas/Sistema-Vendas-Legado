from django.db import models
from suppliers.models import Fornecedor


class Produto(models.Model):
    """
    Product model - equivalent to model/Produto.java
    Maps to tb_produtos table
    """
    descricao = models.CharField('Descrição', max_length=100)
    preco = models.DecimalField('Preço', max_digits=10, decimal_places=2)
    qtd_estoque = models.IntegerField('Quantidade em Estoque')
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.PROTECT,
        verbose_name='Fornecedor',
        related_name='produtos'
    )
    
    class Meta:
        db_table = 'tb_produtos'
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['descricao']
    
    def __str__(self):
        return self.descricao
    
    @property
    def estoque_baixo(self):
        """Check if stock is low (less than or equal to 10)"""
        return self.qtd_estoque <= 10
    
    def adicionar_estoque(self, quantidade):
        """Add stock quantity"""
        self.qtd_estoque += quantidade
        self.save()
    
    def remover_estoque(self, quantidade):
        """Remove stock quantity"""
        if self.qtd_estoque >= quantidade:
            self.qtd_estoque -= quantidade
            self.save()
            return True
        return False
