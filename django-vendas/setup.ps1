# Quick Setup Script for Django Sistema de Vendas
# Run this script in PowerShell to set up the project

Write-Host "=== Sistema de Vendas - Django Setup ===" -ForegroundColor Green
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python is not installed or not in PATH!" -ForegroundColor Red
    exit 1
}
Write-Host "Found: $pythonVersion" -ForegroundColor Green

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists, skipping..." -ForegroundColor Cyan
} else {
    python -m venv venv
    Write-Host "Virtual environment created successfully!" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create .env file if it doesn't exist
Write-Host ""
Write-Host "Checking environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host ".env file already exists, skipping..." -ForegroundColor Cyan
} else {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "IMPORTANT: Edit .env file with your database credentials!" -ForegroundColor Red
}

# Run migrations
Write-Host ""
Write-Host "Running database migrations..." -ForegroundColor Yellow
python manage.py migrate

# Collect static files
Write-Host ""
Write-Host "Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

# Create superuser prompt
Write-Host ""
Write-Host "=== Create Superuser ===" -ForegroundColor Green
Write-Host "You need to create an admin account to access the system." -ForegroundColor Yellow
$createSuperuser = Read-Host "Do you want to create a superuser now? (Y/n)"

if ($createSuperuser -ne "n" -and $createSuperuser -ne "N") {
    python manage.py createsuperuser
}

# Final instructions
Write-Host ""
Write-Host "=== Setup Complete! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit .env file with your database credentials (if not done)"
Write-Host "2. Run: python manage.py runserver"
Write-Host "3. Open browser: http://localhost:8000"
Write-Host ""
Write-Host "Admin panel: http://localhost:8000/admin" -ForegroundColor Cyan
Write-Host ""

# Offer to start server
$startServer = Read-Host "Do you want to start the development server now? (Y/n)"
if ($startServer -ne "n" -and $startServer -ne "N") {
    Write-Host ""
    Write-Host "Starting development server..." -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
    Write-Host ""
    python manage.py runserver
}
