"""
Utility functions - equivalent to model/Utilitarios.java and model/WebServiceCep.java
"""
import requests
from typing import Optional, Dict


def buscar_cep(cep: str) -> Optional[Dict[str, str]]:
    """
    Search for address by CEP using ViaCEP API.
    Equivalent to WebServiceCep.searchCep() from Java version.
    
    Args:
        cep: CEP string (with or without hyphen)
    
    Returns:
        Dictionary with address data or None if not found
    """
    # Remove non-numeric characters
    cep_limpo = ''.join(filter(str.isdigit, cep))
    
    if len(cep_limpo) != 8:
        return None
    
    try:
        # Use ViaCEP API (free Brazilian CEP webservice)
        url = f'https://viacep.com.br/ws/{cep_limpo}/json/'
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if CEP was found
            if 'erro' not in data:
                return {
                    'logradouro': data.get('logradouro', ''),
                    'bairro': data.get('bairro', ''),
                    'cidade': data.get('localidade', ''),
                    'uf': data.get('uf', ''),
                    'complemento': data.get('complemento', ''),
                }
    except Exception as e:
        print(f"Erro ao buscar CEP: {e}")
        return None
    
    return None


def formatar_cep(cep: str) -> str:
    """Format CEP string with hyphen (12345678 -> 12345-678)"""
    cep_limpo = ''.join(filter(str.isdigit, cep))
    if len(cep_limpo) == 8:
        return f'{cep_limpo[:5]}-{cep_limpo[5:]}'
    return cep


def formatar_telefone(telefone: str) -> str:
    """Format phone number (11987654321 -> (11) 98765-4321)"""
    tel_limpo = ''.join(filter(str.isdigit, telefone))
    
    if len(tel_limpo) == 11:  # Cell phone
        return f'({tel_limpo[:2]}) {tel_limpo[2:7]}-{tel_limpo[7:]}'
    elif len(tel_limpo) == 10:  # Landline
        return f'({tel_limpo[:2]}) {tel_limpo[2:6]}-{tel_limpo[6:]}'
    
    return telefone


def formatar_cpf(cpf: str) -> str:
    """Format CPF (12345678901 -> 123.456.789-01)"""
    cpf_limpo = ''.join(filter(str.isdigit, cpf))
    
    if len(cpf_limpo) == 11:
        return f'{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}'
    
    return cpf


def formatar_cnpj(cnpj: str) -> str:
    """Format CNPJ (12345678901234 -> 12.345.678/9012-34)"""
    cnpj_limpo = ''.join(filter(str.isdigit, cnpj))
    
    if len(cnpj_limpo) == 14:
        return f'{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}'
    
    return cnpj


def formatar_moeda(valor: float) -> str:
    """Format currency value (1234.56 -> R$ 1.234,56)"""
    return f'R$ {valor:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.')
