# Sistema de Vendas - Legado - AI Coding Instructions

## Project Overview
Desktop sales management system built with **Java Swing**, **MySQL**, and **Apache Ant**. Legacy NetBeans project following a 3-tier architecture (View → DAO → Database) without modern frameworks.

## Architecture Pattern

### Three-Layer Structure
```
view/ (Swing JFrames) → dao/ (Data Access Objects) → MySQL Database
                    ↓
                  model/ (POJOs + utilities)
```

**Critical**: This is **NOT** an MVC pattern. No Controller layer exists. View components directly instantiate and call DAO methods.

### DAO Pattern
Every DAO class follows this exact structure:
```java
public class DaoCliente {
    private Connection con;
    
    public DaoCliente() {
        this.con = new ConnectionFactory().getConnection();
    }
    
    // CRUD methods: cadastrar*, alterar*, excluir*, listar*
}
```

- DAOs instantiate `ConnectionFactory` in constructor (not dependency injection)
- Use `PreparedStatement` exclusively for SQL
- Show `JOptionPane` dialogs directly from DAO methods for errors/success
- Return `List<T>` for queries, `void` for inserts/updates
- Close statements but **not connections** (connection pooling not implemented)

### Model Classes
Pure POJOs with getters/setters only. Example:
- `Cliente`, `Produto`, `Venda` have primitive fields + related objects
- `ItemVenda` contains `Venda` and `Produto` objects (composition pattern)
- No business logic in models

### View Layer (Swing Forms)
- All forms extend `javax.swing.JFrame`
- NetBeans Form Editor generates GUI code in `initComponents()` (marked `// <editor-fold>`)
- **Never manually edit** code between `//GEN-BEGIN` and `//GEN-END` comments
- Business logic goes in button action handlers (`btnActionPerformed` methods)
- Forms instantiate DAOs directly: `new DaoCliente().cadastrarCliente(obj)`

## Database Connection

### Single Configuration Point
`src/jdbc/ConnectionFactory.java` hardcodes connection details:
```java
private final String ip = "127.0.0.1";
private final String user = "usuario";
private final String pass = "123";
private final String bd = "BDVENDAS";
```

**To change DB settings**: Edit `ConnectionFactory.java` only. Never pass connection strings elsewhere.

### Schema Reference
Database: `BDVENDAS` (MySQL 5.7+)
Key tables: `tb_clientes`, `tb_produtos`, `tb_vendas`, `tb_itensvendas`, `tb_fornecedores`, `tb_funcionarios`

Schema script: `Script BD Vendas/Script Banco BDVendas.sql`

## Development Workflow

### Building (Apache Ant)
```bash
# Clean and rebuild
ant clean build

# Run JAR
java -jar "dist/Sistema Vendas (Resolvido).jar"
```

Build file: `build.xml` (NetBeans-generated, rarely modified)

### Entry Point
Application starts at `view.FrmLogin` (login screen) → `view.FrmMenu` (main menu)

### Adding New Entities
1. Create table in MySQL (`tb_*` naming convention)
2. Create model class (`src/model/*.java`) with getters/setters
3. Create DAO class (`src/dao/Dao*.java`) following existing pattern
4. Create Swing form via NetBeans Form Editor (`src/view/Frm*.java`)
5. Wire form buttons to DAO methods

## Special Integrations

### CEP WebService
`model.WebServiceCep` uses **dom4j XML parser** to fetch addresses from Brazilian postal code API.
- Dependency: `dom4j-2.0.3.jar`
- Used in: `FrmCliente`, `FrmFornecedor` for address auto-fill
- Pattern: `WebServiceCep.searchCep("13345-325")` returns object with parsed address

### Date Handling
- Database stores dates as strings: `"dd/MM/yyyy"` format
- Java 8+ `LocalDate` used in DAOs for date filtering
- Convert with: `date_inicio.toString()` for SQL queries
- Display with: `date_format(v.data_venda,'%d/%m/%Y')` in SQL

## Common Patterns

### List/Search Pattern
```java
// DAO method
public List<Cliente> listarClientes() {
    List<Cliente> lista = new ArrayList<>();
    String sql = "select * from tb_clientes";
    PreparedStatement stmt = con.prepareStatement(sql);
    ResultSet rs = stmt.executeQuery();
    while (rs.next()) {
        Cliente obj = new Cliente();
        obj.setId(rs.getInt("id"));
        // ... set all fields
        lista.add(obj);
    }
    return lista;
}
```

### Sales Transaction Pattern
1. Insert into `tb_vendas` (parent)
2. Get `max(id)` from `tb_vendas` via `DaoVenda.retornaUltimaVenda()`
3. Insert multiple rows into `tb_itensvendas` (children) using returned ID
4. Update `tb_produtos` stock quantities

See: `DaoVenda.cadastrarVenda()` + `DaoItemVenda.cadastraItem()` + stock update logic

## Utilities

`model.Utilitarios` provides:
- `LimpaTela(JPanel)`: Clears all JTextField components in panel
- `verificaLimpo(JPanel)`: Checks if required fields are filled

## Branch Context
Current branch: `login-dev` (working on authentication features)
Default branch: `main`

## Constraints
- **No unit tests** exist in this legacy project
- **No logging framework** - errors print to `System.err` or show in JOptionPane
- **No dependency management** - JARs stored locally (not in repo structure shown)
- Forms are **NetBeans-dependent** - editing `.form` files requires NetBeans IDE
