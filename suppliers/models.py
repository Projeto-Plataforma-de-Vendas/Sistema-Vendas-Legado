from django.db import models


class Fornecedor(models.Model):
    """
    Supplier model - equivalent to model/Fornecedor.java
    Maps to tb_fornecedores table
    """
    nome = models.CharField('Nome', max_length=100)
    cnpj = models.CharField('CNPJ', max_length=20, unique=True)
    email = models.EmailField('E-mail', max_length=200, blank=True)
    telefone = models.CharField('Telefone', max_length=30)
    celular = models.CharField('Celular', max_length=30)
    cep = models.CharField('CEP', max_length=100)
    endereco = models.CharField('Endereço', max_length=255)
    numero = models.IntegerField('Número')
    complemento = models.CharField('Complemento', max_length=200, blank=True)
    bairro = models.CharField('Bairro', max_length=100)
    cidade = models.CharField('Cidade', max_length=100)
    estado = models.CharField('Estado', max_length=2)
    
    class Meta:
        db_table = 'tb_fornecedores'
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
    
    @property
    def endereco_completo(self):
        """Return complete address"""
        return f'{self.endereco}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado}'
