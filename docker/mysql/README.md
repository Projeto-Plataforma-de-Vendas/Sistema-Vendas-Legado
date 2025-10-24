# Docker MySQL Setup

This directory contains the Docker configuration for the MySQL database used by Sistema de Vendas.

## Structure

```
docker/mysql/
├── Dockerfile       # MySQL image definition
└── init.sql        # Database initialization script
```

## How It Works

### Dockerfile

The `Dockerfile` extends the official MySQL 8.0 image and:
- Copies the `init.sql` script to `/docker-entrypoint-initdb.d/`
- Sets default character set to UTF-8 (utf8mb4)

### init.sql

The initialization script automatically runs when the container is first created. It:
- Creates the `BDVENDAS` database if it doesn't exist
- Creates all required tables (clientes, fornecedores, produtos, vendas, etc.)
- Sets up foreign key relationships
- Uses `CREATE TABLE IF NOT EXISTS` for idempotency

### Volume

A Docker volume named `mysql_data` is created to persist database data:
- Data survives container restarts
- Data survives container recreation
- Data is stored in Docker's volume storage

## Environment Variables

The following environment variables are pulled from the `.env` file in the project root:

- `DB_NAME` - Database name (default: BDVENDAS)
- `DB_USER` - MySQL user (default: usuario)
- `DB_PASSWORD` - MySQL password (default: 123)
- `DB_PORT` - Host port mapping (default: 3306)

## Usage

### Start the database

```bash
docker-compose up -d
```

### Check status

```bash
docker-compose ps
```

### View logs

```bash
docker-compose logs -f mysql
```

### Stop the database

```bash
docker-compose down
```

### Remove all data (fresh start)

```bash
docker-compose down -v
docker-compose up -d
```

## Connection

From Django (or any application on the host):
- **Host**: `127.0.0.1` or `localhost`
- **Port**: `3306` (or whatever is set in `DB_PORT`)
- **Database**: `BDVENDAS`
- **User**: `usuario`
- **Password**: `123`

## Healthcheck

The container includes a healthcheck that:
- Runs every 10 seconds
- Attempts to ping MySQL using `mysqladmin`
- Retries up to 5 times
- Waits 30 seconds before first check (startup time)

## Changes from Original Schema

The `init.sql` file has been adapted from the original `Script Banco BDVendas.sql` with the following changes:

1. **CREATE DATABASE IF NOT EXISTS** - Prevents errors on reinitialization
2. **CREATE TABLE IF NOT EXISTS** - Makes script idempotent
3. **Removed CREATE USER and GRANT** - Handled by Docker environment variables
4. **Removed test query** - `select * from tb_clientes where nome like 'a%';`
5. **Added ENGINE and CHARSET** - Explicitly sets InnoDB and UTF-8 encoding
6. **Removed flush privileges** - Not needed with Docker's user management

These changes ensure the script works correctly with Docker's automatic initialization process.

## Troubleshooting

### Port already in use

If you see "port is already allocated" error:

1. Check if local MySQL is running: `netstat -ano | findstr :3306`
2. Stop local MySQL: `Stop-Service MySQL80`
3. Or change `DB_PORT` in `.env` to a different port (e.g., 3307)

### Container not starting

```bash
# Check logs for errors
docker-compose logs mysql

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache mysql
docker-compose up -d
```

### Can't connect from Django

1. Ensure container is running: `docker-compose ps`
2. Wait 30-60 seconds after first start
3. Check healthcheck: `docker-compose ps` (should show "healthy")
4. Verify credentials in `.env` match

### Database not initialized

```bash
# Verify init script is present in container
docker-compose exec mysql ls -la /docker-entrypoint-initdb.d/

# Check initialization logs
docker-compose logs mysql | grep -i "init"
```

## Security Notes

⚠️ **Development Only**: The default credentials (`usuario`/`123`) are for development purposes only.

For production:
- Use strong passwords
- Don't expose port 3306 to the internet
- Use environment-specific `.env` files
- Consider using Docker secrets for sensitive data
- Implement regular backups
