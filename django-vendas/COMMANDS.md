# Django Commands Quick Reference

## 🚀 Getting Started

```powershell
# Navigate to project
cd django-vendas

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run development server
python manage.py runserver

# Run on specific port
python manage.py runserver 8080

# Run on all interfaces (accessible from network)
python manage.py runserver 0.0.0.0:8000
```

## 📦 Database Commands

```powershell
# Create migration files (after model changes)
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Rollback migration
python manage.py migrate <app_name> <migration_name>

# SQL for a migration (without executing)
python manage.py sqlmigrate <app_name> <migration_number>

# Flush database (delete all data)
python manage.py flush
```

## 👤 User Management

```powershell
# Create superuser (admin)
python manage.py createsuperuser

# Change user password
python manage.py changepassword <username>
```

## 🎨 Static Files

```powershell
# Collect all static files
python manage.py collectstatic

# Collect without prompting
python manage.py collectstatic --noinput

# Clear collected static files
python manage.py collectstatic --clear
```

## 🧪 Testing

```powershell
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test customers

# Run specific test class
python manage.py test customers.tests.ClienteTestCase

# Run with verbose output
python manage.py test --verbosity=2

# Keep test database
python manage.py test --keepdb
```

## 🐚 Django Shell

```powershell
# Open Django shell
python manage.py shell

# Open enhanced shell (if django-extensions installed)
python manage.py shell_plus
```

### Shell Examples

```python
# Import models
from customers.models import Cliente
from sales.models import Venda, ItemVenda

# Query all records
clientes = Cliente.objects.all()

# Filter records
clientes_sp = Cliente.objects.filter(estado='SP')

# Get single record
cliente = Cliente.objects.get(id=1)

# Create record
cliente = Cliente.objects.create(
    nome='João Silva',
    cpf='12345678901',
    email='joao@email.com',
    # ... other fields
)

# Update record
cliente.nome = 'João Pedro Silva'
cliente.save()

# Delete record
cliente.delete()

# Count records
total = Cliente.objects.count()

# Aggregate
from django.db.models import Sum
total_vendas = Venda.objects.aggregate(total=Sum('total_venda'))

# Related objects (ForeignKey)
produto = Produto.objects.get(id=1)
fornecedor = produto.fornecedor  # Access related object

# Reverse relationship
fornecedor = Fornecedor.objects.get(id=1)
produtos = fornecedor.produtos.all()  # All products from this supplier
```

## 🔍 Inspection Commands

```powershell
# List all installed apps
python manage.py diffsettings

# Show project structure
python manage.py check

# Database shell
python manage.py dbshell

# Show SQL for models
python manage.py inspectdb

# Show URLs
python manage.py show_urls  # Requires django-extensions
```

## 📝 Custom Commands

```powershell
# Create custom management command
# Create file: <app>/management/commands/<command_name>.py
python manage.py <command_name>
```

## 🌐 Development Utilities

```powershell
# Check for problems
python manage.py check

# Check deployment checklist
python manage.py check --deploy

# Send test email
python manage.py sendtestemail

# Clear cache
python manage.py clear_cache  # Requires django-extensions
```

## 📊 Data Management

```powershell
# Export data to JSON
python manage.py dumpdata > data.json

# Export specific app
python manage.py dumpdata customers > customers.json

# Export with indentation (readable)
python manage.py dumpdata customers --indent 2 > customers.json

# Load data from JSON
python manage.py loaddata data.json

# Load specific fixture
python manage.py loaddata customers.json
```

## 🔐 Security

```powershell
# Generate new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 📦 App Management

```powershell
# Create new app
python manage.py startapp <app_name>

# Create project
django-admin startproject <project_name>
```

## 🌍 Internationalization

```powershell
# Create/update translation files
python manage.py makemessages -l pt_BR

# Compile translations
python manage.py compilemessages
```

## 📈 Performance

```powershell
# Show slow queries (requires django-debug-toolbar)
# Access: /__debug__/ when DEBUG=True

# Profile database queries in shell
from django.db import connection
print(len(connection.queries))  # Number of queries
print(connection.queries)  # Query details
```

## 🐛 Debugging Tips

```python
# In views.py
import pdb; pdb.set_trace()  # Set breakpoint

# Better debugging (install ipdb)
import ipdb; ipdb.set_trace()

# Print SQL query
print(queryset.query)

# Explain query
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("EXPLAIN " + str(queryset.query))
    print(cursor.fetchall())
```

## 🚀 Production Commands

```powershell
# Collect static with production settings
python manage.py collectstatic --settings=config.settings_prod

# Run with Gunicorn (production WSGI server)
gunicorn config.wsgi:application --bind 0.0.0.0:8000

# With workers
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4

# With logging
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --access-logfile - --error-logfile -
```

## 📱 Useful Shortcuts

```powershell
# Shorthand for common commands
python manage.py runserver    # rs (with django-extensions)
python manage.py shell         # sh
python manage.py migrate       # mg
python manage.py makemigrations # mkm
```

## 🔧 Environment Variables

```powershell
# Set environment variable (PowerShell)
$env:DJANGO_SETTINGS_MODULE = "config.settings"

# Set for current session
$env:DEBUG = "False"

# Use .env file (recommended)
# Install python-decouple
pip install python-decouple
```

## 📚 Documentation

```powershell
# Open Django documentation in browser
python -m webbrowser "https://docs.djangoproject.com/"

# Check Django version
python -m django --version
python manage.py --version
```

## 🎯 Common Workflows

### After Model Changes
```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Deploy to Production
```powershell
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### Database Reset (Development)
```powershell
python manage.py flush
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata fixtures/sample_data.json
```

### Fresh Start
```powershell
# Delete migrations
Remove-Item -Recurse -Force */migrations/0*.py

# Delete database (if SQLite)
Remove-Item db.sqlite3

# Recreate
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

## 🆘 Troubleshooting

### Problem: "No module named 'django'"
```powershell
# Solution: Activate virtual environment
.\venv\Scripts\Activate.ps1
```

### Problem: "Table doesn't exist"
```powershell
# Solution: Run migrations
python manage.py migrate
```

### Problem: "Static files not loading"
```powershell
# Solution: Collect static files
python manage.py collectstatic --noinput
```

### Problem: "Module not found"
```powershell
# Solution: Install requirements
pip install -r requirements.txt
```

### Problem: "Permission denied"
```powershell
# Solution: Run PowerShell as Administrator or change execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 💡 Pro Tips

1. **Use `--help`** to see all options for any command:
   ```powershell
   python manage.py runserver --help
   ```

2. **Tab completion** works in Django shell (IPython)

3. **Use django-extensions** for extra commands:
   ```powershell
   pip install django-extensions
   # Add 'django_extensions' to INSTALLED_APPS
   python manage.py shell_plus  # Enhanced shell
   python manage.py show_urls   # List all URLs
   python manage.py graph_models # Generate model diagram
   ```

4. **Debug toolbar** for development:
   ```powershell
   pip install django-debug-toolbar
   # Configure in settings.py
   # Access at /__debug__/ when DEBUG=True
   ```

5. **Keep virtual environment activated** while working:
   ```powershell
   # Your prompt should show (venv) prefix
   (venv) PS C:\...\django-vendas>
   ```

---

**Tip**: Bookmark this file for quick reference!
**More**: https://docs.djangoproject.com/en/4.2/ref/django-admin/
