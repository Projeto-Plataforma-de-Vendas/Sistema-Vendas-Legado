# MySQL Dockerfile for Sistema de Vendas
FROM mysql:8.0

# Copy initialization script
COPY init.sql /docker-entrypoint-initdb.d/

# Set default character set and collation
ENV MYSQL_CHARSET=utf8mb4
ENV MYSQL_COLLATION=utf8mb4_unicode_ci
