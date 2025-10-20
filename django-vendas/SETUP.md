# SETUP GUIDE - Django Sistema de Vendas

## Prerequisites

- Python 3.10 or higher
- MySQL 5.7 or higher
- pip (Python package installer)
- Git (optional)

## Step-by-Step Installation

### 1. Navigate to the Django project folder

```powershell
cd "C:\Users\user\OneDrive\Documentos\Biopark\mod-tech\Sistema-Vendas-Legado\django-vendas"
```

### 2. Create a virtual environment

```powershell
python -m venv venv
```

### 3. Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

### 5. Configure environment variables

Copy the example environment file:
```powershell
Copy-Item .env.example .env
```

Edit `.env` file with your database credentials:
```
DB_NAME=BDVENDAS
DB_USER=usuario
DB_PASSWORD=123
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 6. Ensure MySQL database exists

The database `BDVENDAS` should already exist from the Java version.
If not, create it:

```sql
CREATE DATABASE BDVENDAS CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 7. Run migrations

Django will use the existing tables defined in the models:

```powershell
python manage.py migrate
```

### 8. Create a superuser (admin account)

```powershell
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 9. Collect static files

```powershell
python manage.py collectstatic --noinput
```

### 10. Run the development server

```powershell
python manage.py runserver
```

### 11. Access the application

Open your browser and navigate to:
- **Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin

## Testing the Migration

### Verify Database Compatibility

The Django models are designed to work with the existing MySQL tables:

- `tb_clientes` → `customers.Cliente`
- `tb_fornecedores` → `suppliers.Fornecedor`
- `tb_produtos` → `inventory.Produto`
- `tb_vendas` → `sales.Venda`
- `tb_itensvendas` → `sales.ItemVenda`
- `tb_funcionarios` → `accounts.Funcionario`

### Create Test Data (if database is empty)

You can use the Django admin panel to create test data or use the Django shell:

```powershell
python manage.py shell
```

```python
from customers.models import Cliente

cliente = Cliente.objects.create(
    nome="João Silva",
    cpf="12345678901",
    email="joao@email.com",
    telefone="1140041000",
    celular="11987654321",
    cep="01310-100",
    endereco="Av. Paulista",
    numero=1000,
    bairro="Bela Vista",
    cidade="São Paulo",
    estado="SP"
)
```

## Common Issues

### Issue: Import errors for crispy_forms

**Solution**: Make sure crispy-bootstrap5 is installed:
```powershell
pip install crispy-bootstrap5
```

### Issue: MySQL connection errors

**Solution**: 
1. Verify MySQL is running
2. Check credentials in `.env` file
3. Ensure `mysqlclient` is installed: `pip install mysqlclient`

### Issue: Static files not loading

**Solution**: 
```powershell
python manage.py collectstatic --noinput
```

### Issue: Permission errors on Windows

**Solution**: Run PowerShell as Administrator or adjust execution policy:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Development Workflow

### Running Tests

```powershell
python manage.py test
```

### Creating Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

### Accessing Django Shell

```powershell
python manage.py shell
```

### Creating Sample Data

```powershell
python manage.py loaddata fixtures/sample_data.json
```

## Architecture Comparison

| Component | Java Swing | Django |
|-----------|-----------|---------|
| **Pattern** | 3-tier (View→DAO→DB) | MVT (Model-View-Template) |
| **UI** | Swing JFrames | HTML/CSS/Bootstrap |
| **Database** | JDBC + SQL | Django ORM |
| **Forms** | NetBeans Form Editor | Django Forms + Crispy Forms |
| **Validation** | Manual in DAOs | Django Form Validation |
| **Auth** | Custom login form | Django Auth Framework |
| **Routing** | N/A (desktop) | URL patterns |
| **Session** | N/A | Django Sessions |

## Key Features Implemented

✅ Authentication system (login/logout)
✅ Dashboard with statistics
✅ CRUD for Customers (Clientes)
✅ CRUD for Suppliers (Fornecedores)
✅ CRUD for Products (Produtos)
✅ CRUD for Employees (Funcionários)
✅ Sales management with items
✅ Stock control
✅ Sales history and reports
✅ CEP lookup integration (WebService)
✅ Input validation and masks
✅ Responsive design (Bootstrap 5)

## Next Steps

1. Add more templates for other entities (suppliers, products, etc.)
2. Implement sales creation form with dynamic item formsets
3. Add PDF report generation
4. Implement user permissions based on `nivel_acesso`
5. Add data visualization (charts for sales)
6. Deploy to production (Heroku, AWS, etc.)

## Production Deployment

For production, consider:

1. Set `DEBUG=False` in settings
2. Configure proper `SECRET_KEY`
3. Use environment-specific settings
4. Set up proper static file serving (Nginx, Whitenoise)
5. Configure HTTPS
6. Set up proper database backups
7. Use Gunicorn or uWSGI as WSGI server

Example production command:
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```
