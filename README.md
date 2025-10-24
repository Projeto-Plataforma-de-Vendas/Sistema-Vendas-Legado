# Sistema de Vendas - Django

Sistema de gestão de vendas desenvolvido em Django 4.2, migrado do sistema legado Java Swing e integrado a um banco MySQL executado via Docker.

## Tecnologias

- Python 3.10+
- Django 4.2
- MySQL 8.0 (container Docker)
- Bootstrap 5
- jQuery
- Docker & Docker Compose

## Requisitos

- Python 3.10 ou superior
- Docker Desktop com Docker Compose
- pip
- Git
- Microsoft C++ Build Tools (compilação do `mysqlclient`)

## Guia de Configuração

### 1. Clonar o repositório

```powershell
git clone <repository-url>
cd Sistema-Vendas-Legado
```

### 2. Criar o ambiente virtual

```powershell
python -m venv venv
```

### 3. Ativar o ambiente virtual

```powershell
.\venv\Scripts\Activate.ps1
```

Caso apareça erro de política de execução:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Instalar as dependências Python

```powershell
pip install -r requirements.txt
```

### 5. Configurar variáveis de ambiente

Copie o arquivo de exemplo:

```powershell
Copy-Item .env.example .env
```

Edite o `.env` (utilize as credenciais padrão do container Docker caso não tenha ajustes específicos):

```
DB_NAME=BDVENDAS
DB_USER=usuario
DB_PASSWORD=123
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 6. Subir o MySQL com Docker

```powershell
docker-compose up -d
```

O compose irá construir a imagem, criar o volume persistente e inicializar o banco com o schema legado. Aguarde cerca de 1 minuto até que o serviço esteja pronto:

```powershell
docker-compose logs -f mysql
```

Pressione `Ctrl+C` após visualizar a mensagem `ready for connections`.

### 7. Aplicar migrações

```powershell
python manage.py migrate
```

### 8. Criar um superusuário

```powershell
python manage.py createsuperuser
```

### 9. Coletar arquivos estáticos (opcional para desenvolvimento)

```powershell
python manage.py collectstatic --noinput
```

### 10. Executar o servidor de desenvolvimento

```powershell
python manage.py runserver
```

### 11. Acessar a aplicação

- Sistema: http://localhost:8000
- Admin: http://localhost:8000/admin

## Testes e Fluxo de Desenvolvimento

```powershell
# Criar novas migrações
python manage.py makemigrations

# Executar testes automatizados
python manage.py test

# Shell interativo Django
python manage.py shell

# Carregar dados de exemplo
python manage.py loaddata fixtures/sample_data.json
```

## Gerenciamento do Docker

```powershell
# Iniciar banco
docker-compose up -d

# Parar banco
docker-compose down

# Ver logs
docker-compose logs -f mysql

# Abrir shell MySQL
docker-compose exec mysql mysql -u usuario -p123 BDVENDAS

# Backup do banco
docker-compose exec mysql mysqldump -u usuario -p123 BDVENDAS > backup.sql

# Restaurar backup
Get-Content backup.sql | docker-compose exec -T mysql mysql -u usuario -p123 BDVENDAS

# Resetar dados
docker-compose down -v
docker-compose up -d
```

O volume nomeado `mysql_data` garante a persistência entre reinicializações. Para um reset completo utilize o bloco "Resetar dados" acima.

## Solução de Problemas

- **Erro ao importar `crispy_forms`** → Instale `crispy-bootstrap5` com `pip install crispy-bootstrap5`.
- **Falha de conexão com o banco** → Confirme se o container está ativo (`docker-compose ps`), valide o `.env` e aguarde a inicialização completa registrada nos logs.
- **Arquivos estáticos ausentes** → Execute `python manage.py collectstatic --noinput`.
- **Permissões no Windows** → Rode o PowerShell como administrador ou ajuste a política com `Set-ExecutionPolicy RemoteSigned`.

## Arquitetura

Aplicação web seguindo o padrão MVT (Model-View-Template) do Django.

### Apps Django

- **core**: funcionalidades centrais, autenticação, dashboard
- **customers**: gestão de clientes
- **suppliers**: gestão de fornecedores
- **inventory**: gestão de produtos e estoque
- **sales**: gestão de vendas e itens
- **accounts**: gestão de funcionários e usuários

### Fluxo MVT

```
Model (models.py) → View (views.py) → Template (templates/)
                ↓
            Database (MySQL)
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
├── accounts/
├── config/
├── core/
├── customers/
├── docker/
│   └── mysql/
├── inventory/
├── sales/
├── suppliers/
├── static/
├── templates/
├── manage.py
└── README.md
```

## Diferenças em relação ao sistema legado

| Aspecto | Java Swing | Django |
|---------|-----------|--------|
| Interface | Desktop (Swing) | Web (HTML/CSS/JS) |
| Padrão | 3-tier (View→DAO→DB) | MVT (Model-View-Template) |
| Persistência | JDBC + SQL direto | Django ORM |
| Autenticação | Custom | Django Auth |
| Validação | Manual | Django Forms |
| Roteamento | N/A | URL patterns |

## Licença

Projeto educacional - Eng. Software - 4° Período - Grupo 2 - Biopark
