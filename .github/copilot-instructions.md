# Sistema de Vendas - Django - AI Coding Instructions

## Project Overview
Web-based sales management system built with **Django 4.2**, **MySQL**, and **Bootstrap 5**. Modern web application following Django's **MVT (Model-View-Template)** architecture pattern, migrated from a legacy Java Swing desktop application.

## Architecture Pattern

### MVT Structure
```
Model (models.py) → View (views.py) → Template (HTML/DTL)
                ↓
        MySQL Database (via Django ORM)
```

**Key Principles**:
- Models define database schema using Django ORM (no raw SQL unless necessary)
- Views handle business logic and HTTP request/response
- Templates render HTML using Django Template Language (DTL)
- Forms handle validation and data sanitization
- URL patterns route requests to appropriate views

## Django Apps Structure

The project is organized into the following Django apps:

### Core Apps
- **config/**: Project-wide settings, URLs, WSGI/ASGI configuration
- **core/**: Authentication, dashboard, utilities (CEP lookup, formatters)
- **accounts/**: User management (funcionários/employees)
- **customers/**: Customer management (clientes)
- **suppliers/**: Supplier management (fornecedores)
- **inventory/**: Product and stock management (produtos/estoque)
- **sales/**: Sales processing and reporting (vendas)

### Model Pattern

- **Models**: Django ORM models mapping to MySQL tables (e.g., `Cliente`, `Produto`, `Venda`)
- **Views**: Function-based views (FBVs) handling HTTP requests
- **Forms**: Django ModelForms for validation
- **Templates**: HTML templates with Django Template Language
- **URLs**: URL patterns for routing

### Django ORM Pattern
```python
# Model definition
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=20, unique=True)
    # ... other fields
    
    class Meta:
        db_table = 'tb_clientes'
```

### View Pattern
```python
# Function-based view
def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'customers/cliente_list.html', {'clientes': clientes})

def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente cadastrado com sucesso!')
            return redirect('customers:cliente_list')
    else:
        form = ClienteForm()
    return render(request, 'customers/cliente_form.html', {'form': form})
```

## Database Configuration

### Environment Variables
Database settings are configured via `.env` file:
```
DB_NAME=BDVENDAS
DB_USER=usuario
DB_PASSWORD=123
DB_HOST=127.0.0.1
DB_PORT=3306
```

### Schema Reference
Database: `BDVENDAS` (MySQL 5.7+)
Key tables: `tb_clientes`, `tb_produtos`, `tb_vendas`, `tb_itensvendas`, `tb_fornecedores`, `tb_funcionarios`

Schema script: `Script BD Vendas/Script Banco BDVendas.sql`

## Development Workflow

### Running the Server
```bash
# Activate virtual environment
venv\Scripts\Activate.ps1  # Windows

# Run development server
python manage.py runserver
```

### Common Commands
```bash
# Migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test
```

### Adding New Features
1. Create/modify models in `models.py`
2. Create/update forms in `forms.py`
3. Create/update views in `views.py`
4. Create/update templates in `templates/`
5. Wire URL patterns in `urls.py`
6. Run migrations if models changed

## Special Features

### CEP WebService
`core.utils.buscar_cep()` function fetches addresses from Brazilian postal code API.
- Used in: Customer and Supplier forms
- Pattern: `buscar_cep("13345-325")` returns dict with address data
- Integrated via AJAX in forms

### Authentication
- Django's built-in authentication system
- Login required decorator for protected views
- Custom login/logout views in `core` app
- User model linked to `Funcionario` model

## Common Patterns

### List/Search Pattern
```python
# View with filtering
def cliente_list(request):
    nome = request.GET.get('nome', '')
    if nome:
        clientes = Cliente.objects.filter(nome__icontains=nome)
    else:
        clientes = Cliente.objects.all()
    return render(request, 'customers/cliente_list.html', {'clientes': clientes})
```

### Sales Transaction Pattern
1. Create `Venda` object (sale header)
2. Create multiple `ItemVenda` objects (sale items)
3. Update `Produto` stock quantities
4. All operations wrapped in Django transaction

See: `sales/views.py` → `venda_create` view

## Template Structure

### Base Template
`templates/base.html` provides:
- Bootstrap 5 layout
- Navigation menu
- Message display
- Block structure for content

### App Templates
Each app has its own `templates/<app_name>/` folder:
- `*_list.html`: List/table views
- `*_form.html`: Create/edit forms
- `*_detail.html`: Detail views
- `*_confirm_delete.html`: Delete confirmations

## Static Files

### Organization
```
static/
├── css/
│   └── style.css          # Custom styles
└── js/
    └── script.js          # Custom JavaScript
```

### Bootstrap & jQuery
Loaded via CDN in `base.html`

## Testing

Run tests with:
```bash
python manage.py test
```

Each app can have a `tests.py` file for unit tests.

## Branch Context
Current branch: `login-dev` (working on authentication features)
Default branch: `main`

## Migration from Java Swing

This project was migrated from a Java Swing desktop application. Key differences:
- Desktop (Swing) → Web (Django)
- 3-tier (View→DAO→DB) → MVT (Model-View-Template)
- JDBC + SQL → Django ORM
- Custom auth → Django auth
- Manual validation → Django forms

For migration details, see `MIGRATION_COMPLETE.md` and `MIGRATION_NOTES.md`.

## Constraints
- **No unit tests** exist in this legacy project
- **No logging framework** - errors print to `System.err` or show in JOptionPane
- **No dependency management** - JARs stored locally (not in repo structure shown)
- Forms are **NetBeans-dependent** - editing `.form` files requires NetBeans IDE
