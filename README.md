# Sistema de Vendas - Django

Sistema de gestão de vendas desenvolvido com Django, migrado do sistema legado Java Swing.

## Tecnologias

- Python 3.10+
- Django 4.2
- MySQL 5.7+
- Bootstrap 5
- jQuery

## Arquitetura

Aplicação web seguindo o padrão MVT (Model-View-Template) do Django:

### Apps Django

- **core**: Funcionalidades centrais, autenticação, dashboard
- **customers**: Gestão de clientes
- **suppliers**: Gestão de fornecedores
- **inventory**: Gestão de produtos e estoque
- **sales**: Gestão de vendas e itens de venda
- **accounts**: Gestão de funcionários e usuários

### Estrutura MVT

```
Model (models.py) → View (views.py) → Template (templates/)
                ↓
            Database (MySQL)
```

## Instalação

### 1. Clone o repositório

```bash
git clone <repository-url>
cd Sistema-Vendas-Legado
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

Copie o arquivo `.env.example` para `.env` e configure suas credenciais:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações de banco de dados.

### 5. Execute as migrações

```bash
python manage.py migrate
```

### 6. Crie um superusuário

```bash
python manage.py createsuperuser
```

### 7. Execute o servidor

```bash
python manage.py runserver
```

Acesse http://localhost:8000

## Funcionalidades

- ✅ Autenticação de usuários
- ✅ Dashboard com estatísticas
- ✅ CRUD de Clientes
- ✅ CRUD de Fornecedores
- ✅ CRUD de Produtos
- ✅ CRUD de Funcionários
- ✅ Gestão de Vendas
- ✅ Controle de Estoque
- ✅ Histórico de Vendas
- ✅ Relatórios
- ✅ Integração com WebService de CEP

## Estrutura do Projeto

```
Sistema-Vendas-Legado/
├── config/              # Configurações do Django
├── core/                # App central
├── customers/           # App de clientes
├── suppliers/           # App de fornecedores
├── inventory/           # App de produtos/estoque
├── sales/               # App de vendas
├── accounts/            # App de funcionários
├── static/              # Arquivos estáticos (CSS, JS, imagens)
├── templates/           # Templates globais
├── Script BD Vendas/    # Scripts do banco de dados MySQL
└── manage.py
```

## Diferenças do Sistema Legado

| Aspecto | Java Swing | Django |
|---------|-----------|---------|
| Interface | Desktop (Swing) | Web (HTML/CSS/JS) |
| Padrão | 3-tier (View→DAO→DB) | MVT (Model-View-Template) |
| Persistência | JDBC + SQL direto | Django ORM |
| Autenticação | Custom | Django Auth |
| Validação | Manual | Django Forms |
| Roteamento | N/A | URL patterns |

## Comandos Úteis

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic

# Executar testes
python manage.py test

# Shell interativo
python manage.py shell
```

## Licença

Projeto educacional - Biopark
