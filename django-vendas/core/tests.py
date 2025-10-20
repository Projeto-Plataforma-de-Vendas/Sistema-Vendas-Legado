from django.test import TestCase
from .utils import buscar_cep, formatar_cep, formatar_telefone, formatar_cpf, formatar_cnpj, formatar_moeda


class UtilsTestCase(TestCase):
    """Test utility functions"""
    
    def test_formatar_cep(self):
        self.assertEqual(formatar_cep('12345678'), '12345-678')
        self.assertEqual(formatar_cep('12345-678'), '12345-678')
    
    def test_formatar_telefone(self):
        self.assertEqual(formatar_telefone('11987654321'), '(11) 98765-4321')
        self.assertEqual(formatar_telefone('1140041000'), '(11) 4004-1000')
    
    def test_formatar_cpf(self):
        self.assertEqual(formatar_cpf('12345678901'), '123.456.789-01')
    
    def test_formatar_cnpj(self):
        self.assertEqual(formatar_cnpj('12345678901234'), '12.345.678/9012-34')
    
    def test_formatar_moeda(self):
        self.assertEqual(formatar_moeda(1234.56), 'R$ 1.234,56')
