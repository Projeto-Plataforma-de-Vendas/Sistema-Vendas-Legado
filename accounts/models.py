from django.db import models
from django.contrib.auth.models import User


class Funcionario(models.Model):
    """
    Employee model - equivalent to model/Funcionario.java
    Maps to tb_funcionarios table
    Links to Django's User model for authentication
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        null=True,
        blank=True
    )
    nome = models.CharField('Nome', max_length=100)
    rg = models.CharField('RG', max_length=30, blank=True)
    cpf = models.CharField('CPF', max_length=20, unique=True)
    email = models.EmailField('E-mail', max_length=200)
    # using Django's User.password for authentication
    cargo = models.CharField('Cargo', max_length=100)
    nivel_acesso = models.CharField('Nível de Acesso', max_length=50)
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
        db_table = 'tb_funcionarios'
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
    
    @property
    def endereco_completo(self):
        """Return complete address"""
        return f'{self.endereco}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado}'
