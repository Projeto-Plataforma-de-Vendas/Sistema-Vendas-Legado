# 🧪 Quick Testing Guide

## Prerequisites

1. **Virtual Environment Active**
   ```powershell
   cd django-vendas
   .venv\Scripts\Activate.ps1
   ```

2. **Database Configured**
   - Edit `config/settings.py` with your MySQL credentials
   - Or use `.env` file (recommended)

3. **Migrations Applied**
   ```powershell
   python manage.py migrate
   ```

4. **Superuser Created**
   ```powershell
   python manage.py createsuperuser
   # Username: admin
   # Email: admin@example.com
   # Password: (your choice)
   ```

---

## 🚀 Quick Start

### 1. Start Server
```powershell
python manage.py runserver
```

### 2. Access Application
Open browser: http://localhost:8000/

### 3. Login
Use superuser credentials created above

---

## 📝 Testing Workflow

### Test Order (Recommended)

#### 1️⃣ Test Employees First
**Why**: Needed for system users

1. Go to **Funcionários** → **Cadastrar**
2. Fill in employee data
3. Test CEP lookup (use: 13345-325)
4. Save and verify in list
5. Edit and update
6. Search functionality

#### 2️⃣ Test Suppliers
**Why**: Needed for products

1. Go to **Fornecedores** → **Cadastrar**
2. Add supplier (e.g., "Distribuidora ABC")
3. CNPJ: 12.345.678/0001-90
4. Test CEP lookup
5. Save and verify

#### 3️⃣ Test Products
**Why**: Needed for sales

1. Go to **Produtos** → **Cadastrar**
2. Add products (e.g., "Notebook Dell", "Mouse Logitech")
3. Set initial stock (e.g., 50 units)
4. Set prices
5. Associate with supplier
6. Save multiple products
7. Check **Estoque** view

#### 4️⃣ Test Customers
1. Go to **Clientes** → **Cadastrar**
2. Add customer
3. Test CEP lookup
4. Save and verify

#### 5️⃣ Test Sales (Complex)
1. Go to **Vendas** → **Nova Venda**
2. Select customer
3. Add multiple items:
   - Click "Adicionar Item" to add rows
   - Select products
   - Set quantities
4. Submit sale
5. Verify:
   - Sale detail shows correct items
   - Stock decreased in Products list
   - Total calculated correctly

#### 6️⃣ Test Sales History
1. Go to **Vendas** → **Histórico**
2. Filter by date
3. View details
4. Check totals

#### 7️⃣ Test Sales Report
1. Go to **Vendas** → **Total de Vendas**
2. Set date range
3. Verify total calculations

#### 8️⃣ Test Delete with Stock Restoration
1. Go to **Vendas** → **Histórico**
2. Delete a sale
3. Check that stock was restored in **Produtos**

---

## 🎯 Feature Testing Checklist

### Authentication
- [ ] Login works
- [ ] Logout works
- [ ] Cannot access pages without login
- [ ] User name shows in navbar

### Customers (Clientes)
- [ ] List displays
- [ ] Search works
- [ ] Create customer
- [ ] CEP lookup auto-fills address
- [ ] Edit customer
- [ ] Delete customer
- [ ] Pagination works (if > 20 records)

### Suppliers (Fornecedores)
- [ ] List displays
- [ ] Search works
- [ ] Create supplier
- [ ] CEP lookup works
- [ ] Edit supplier
- [ ] Delete supplier
- [ ] Pagination works

### Products (Produtos)
- [ ] List displays with stock
- [ ] Low stock shows warning (≤10)
- [ ] Search works
- [ ] Create product
- [ ] Edit product
- [ ] Delete product
- [ ] Stock view works
- [ ] Stock statistics display

### Sales (Vendas)
- [ ] Can create sale with 1 item
- [ ] Can add multiple items dynamically
- [ ] Can remove items
- [ ] Stock decreases on sale
- [ ] Total calculates correctly
- [ ] Sale detail shows all info
- [ ] Sales list shows history
- [ ] Date filter works
- [ ] Delete restores stock
- [ ] Total sales report works
- [ ] Cannot sell more than stock (validation)

### Employees (Funcionários)
- [ ] List displays
- [ ] Search works
- [ ] Create employee
- [ ] CEP lookup works
- [ ] Edit employee
- [ ] Delete employee
- [ ] Access level displays correctly

### UI/UX
- [ ] Navigation menu works
- [ ] All icons display
- [ ] Messages appear (success/error)
- [ ] Forms validate
- [ ] Required fields enforce validation
- [ ] Date inputs work
- [ ] Dropdowns populate
- [ ] Tables are responsive
- [ ] Cards display correctly

---

## 🐛 Common Issues & Solutions

### Issue: "No module named 'crispy_forms'"
**Solution**:
```powershell
pip install django-crispy-forms crispy-bootstrap5
```

### Issue: "OperationalError: (1045, Access denied)"
**Solution**: Check database credentials in `config/settings.py`

### Issue: "Table doesn't exist"
**Solution**: Run migrations
```powershell
python manage.py migrate
```

### Issue: "Static files not loading"
**Solution**: Collect static files
```powershell
python manage.py collectstatic
```

### Issue: "CEP lookup not working"
**Solution**: Check internet connection (uses ViaCEP API)

### Issue: "Cannot add items in sale form"
**Solution**: Make sure JavaScript is enabled in browser

---

## 📊 Sample Test Data

### Sample Customer
```
Nome: João da Silva
CPF: 123.456.789-00
Email: joao@email.com
Telefone: (11) 3456-7890
Celular: (11) 98765-4321
CEP: 01310-100 (Avenida Paulista, São Paulo)
```

### Sample Supplier
```
Nome: Distribuidora TechPlus
CNPJ: 12.345.678/0001-90
Email: contato@techplus.com
Telefone: (11) 2222-3333
Celular: (11) 99999-8888
CEP: 01310-100
```

### Sample Products
```
1. Notebook Dell Inspiron - R$ 3500.00 - Stock: 20
2. Mouse Logitech MX - R$ 250.00 - Stock: 50
3. Teclado Mecânico - R$ 450.00 - Stock: 30
4. Monitor LG 24" - R$ 800.00 - Stock: 15
5. Webcam Full HD - R$ 350.00 - Stock: 8 (low stock alert)
```

### Sample Sale
```
Customer: João da Silva
Date: Today
Items:
  - Notebook Dell Inspiron x 1 = R$ 3500.00
  - Mouse Logitech MX x 2 = R$ 500.00
  - Teclado Mecânico x 1 = R$ 450.00
Total: R$ 4450.00
```

---

## ✅ Success Criteria

Application is ready when:

1. ✅ All CRUD operations work for all modules
2. ✅ Sales transaction completes successfully
3. ✅ Stock updates correctly
4. ✅ Delete operations work with confirmations
5. ✅ Search and filters work
6. ✅ Pagination works
7. ✅ Messages display correctly
8. ✅ No console errors
9. ✅ UI renders properly on different screen sizes
10. ✅ CEP lookup works

---

## 🎬 Video Walkthrough Script

### 1. Login (30s)
- Show login page
- Enter credentials
- Redirect to dashboard

### 2. Dashboard (30s)
- Show statistics
- Navigate through menu

### 3. Create Data (2min)
- Create supplier
- Create products
- Create customer

### 4. Make Sale (1min)
- New sale
- Add items
- Submit
- Show detail

### 5. Reports (1min)
- Sales history
- Total sales
- Stock view

### 6. Delete & Restore (30s)
- Delete sale
- Show stock restored

**Total**: ~5 minutes

---

## 📸 Screenshots Checklist

Capture screenshots of:
- [ ] Login page
- [ ] Dashboard
- [ ] Customer list
- [ ] Customer form
- [ ] Supplier list
- [ ] Product list with stock
- [ ] Stock view
- [ ] New sale form (with items)
- [ ] Sale detail
- [ ] Sales history
- [ ] Total sales report
- [ ] Employee list
- [ ] Delete confirmation
- [ ] Success message

---

## 🔐 Security Testing

- [ ] Cannot access without login
- [ ] Session expires after logout
- [ ] CSRF token present in forms
- [ ] SQL injection prevented (use ' OR 1=1 in search)
- [ ] XSS prevented (use <script> in inputs)
- [ ] Password hashed in database

---

## 🚀 Performance Testing

- [ ] Pages load < 2 seconds
- [ ] Search returns results quickly
- [ ] Pagination handles 1000+ records
- [ ] No N+1 queries (check console)
- [ ] Static files load properly

---

**Ready to Test!** 🎉

Start with the Quick Start section and follow the Testing Workflow in order.
