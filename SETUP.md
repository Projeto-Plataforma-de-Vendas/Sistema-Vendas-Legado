# SETUP GUIDE - Django Sistema de Vendas

## Prerequisites

- Python 3.10 or higher
- Docker and Docker Compose (recommended) OR MySQL 5.7 or higher
- pip
- Git
- Microsoft C++ Build Tools (for mysqlclient)

## Step-by-Step Installation

### 1. Navigate to the project folder

```powershell
cd "C:\Users\user\OneDrive\Documentos\Biopark\mod-tech\Sistema-Vendas-Legado"
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

### 6. Setup MySQL Database

#### Option A: Using Docker (Recommended)

Start the MySQL container using docker-compose:

```powershell
docker-compose up -d
```

This will:
- Build the MySQL image with the schema
- Create a persistent volume for data storage
- Initialize the database with all tables
- Start the container in the background

Check if the container is running:
```powershell
docker-compose ps
```

Wait for the database to be ready (usually 30-60 seconds on first run):
```powershell
docker-compose logs -f mysql
```

Press `Ctrl+C` when you see "ready for connections".

#### Option B: Using Local MySQL Installation

If you prefer to use a local MySQL installation instead of Docker:

1. Ensure MySQL is running
2. Create the database:
```sql
CREATE DATABASE BDVENDAS CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
3. Run the schema script from `Script BD Vendas/Script Banco BDVendas.sql`
4. Make sure your `.env` file points to `DB_HOST=127.0.0.1`

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

## Docker Management

### Starting the Database

```powershell
docker-compose up -d
```

### Stopping the Database

```powershell
docker-compose down
```

### Viewing Logs

```powershell
docker-compose logs -f mysql
```

### Accessing MySQL Shell

```powershell
docker-compose exec mysql mysql -u usuario -p123 BDVENDAS
```

### Backup Database

```powershell
docker-compose exec mysql mysqldump -u usuario -p123 BDVENDAS > backup.sql
```

### Restore Database

```powershell
Get-Content backup.sql | docker-compose exec -T mysql mysql -u usuario -p123 BDVENDAS
```

### Removing All Data (Fresh Start)

```powershell
docker-compose down -v
docker-compose up -d
```

## Troubleshooting

### Docker Issues

**Problem**: Port 3306 already in use
```powershell
# Check what's using port 3306
netstat -ano | findstr :3306

# Stop local MySQL service
Stop-Service MySQL80  # Adjust service name as needed

# Or change DB_PORT in .env to use a different port (e.g., 3307)
```

**Problem**: Container fails to start
```powershell
# Check container logs
docker-compose logs mysql

# Rebuild the image
docker-compose build --no-cache mysql
docker-compose up -d
```

**Problem**: Database not initializing
```powershell
# Ensure the init.sql is being copied
docker-compose down -v
docker-compose build mysql
docker-compose up -d
```

### Django Issues

**Problem**: Can't connect to database
- Ensure Docker container is running: `docker-compose ps`
- Check `.env` file has correct credentials
- Wait 30-60 seconds after starting container for first time
- Verify connection: `docker-compose exec mysql mysqladmin ping -u usuario -p123`

**Problem**: Migration errors
```powershell
# Reset migrations (only in development!)
python manage.py migrate --fake-initial
```

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
