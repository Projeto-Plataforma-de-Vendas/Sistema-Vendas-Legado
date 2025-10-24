# Sistema de Vendas - Django

Sistema de gestão de vendas desenvolvido com Django, migrado do sistema legado Java Swing.

## Tecnologias

- Python 3.10+
- Django 4.2
- MySQL 8.0 (Docker)
- Bootstrap 5
- jQuery
- Docker & Docker Compose

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

#### Opção A: Usando Docker (Recomendado)

Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

Inicie o container MySQL:

```bash
docker-compose up -d
```

O Docker irá:
- Construir a imagem MySQL com o schema
- Criar um volume persistente para os dados
- Inicializar o banco de dados com todas as tabelas
- Aguarde 30-60 segundos para o banco ficar pronto

#### Opção B: MySQL Local

Se preferir usar MySQL instalado localmente:

1. Instale MySQL 5.7+ ou 8.0+
2. Configure as credenciais no arquivo `.env`
3. Execute o script `Script BD Vendas/Script Banco BDVendas.sql`

### 5. Crie as tabelas e Execute as migrações

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

## Gerenciamento do Docker

### Comandos Básicos

```bash
# Iniciar banco de dados
docker-compose up -d

# Parar banco de dados
docker-compose down

# Ver logs do MySQL
docker-compose logs -f mysql

# Acessar shell do MySQL
docker-compose exec mysql mysql -u usuario -p123 BDVENDAS

# Backup do banco
docker-compose exec mysql mysqldump -u usuario -p123 BDVENDAS > backup.sql

# Restaurar backup
Get-Content backup.sql | docker-compose exec -T mysql mysql -u usuario -p123 BDVENDAS
```

### Volume de Dados

O Docker cria um volume persistente chamado `mysql_data` que armazena todos os dados do banco de dados. Isso garante que seus dados não sejam perdidos quando o container é parado ou recriado.

Para remover completamente os dados (fresh start):
```bash
docker-compose down -v
```

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
