"""
Script to update database schema for inventory improvements
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def check_and_update_schema():
    with connection.cursor() as cursor:
        # Verificar se o campo estoque_minimo existe
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'BDVENDAS' 
            AND TABLE_NAME = 'tb_produtos' 
            AND COLUMN_NAME = 'estoque_minimo'
        """)
        
        if not cursor.fetchone():
            print("Adicionando campo 'estoque_minimo' à tabela 'tb_produtos'...")
            cursor.execute("""
                ALTER TABLE tb_produtos 
                ADD COLUMN estoque_minimo INTEGER NOT NULL DEFAULT 10
            """)
            print("✓ Campo 'estoque_minimo' adicionado com sucesso!")
        else:
            print("✓ Campo 'estoque_minimo' já existe.")
        
        # Verificar se a tabela tb_movimentacoes_estoque existe
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'BDVENDAS' 
            AND TABLE_NAME = 'tb_movimentacoes_estoque'
        """)
        
        if not cursor.fetchone():
            print("Criando tabela 'tb_movimentacoes_estoque'...")
            cursor.execute("""
                CREATE TABLE tb_movimentacoes_estoque (
                    id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
                    tipo VARCHAR(10) NOT NULL,
                    quantidade INTEGER NOT NULL,
                    quantidade_anterior INTEGER NOT NULL,
                    quantidade_atual INTEGER NOT NULL,
                    data_movimentacao DATETIME(6) NOT NULL,
                    observacao LONGTEXT NOT NULL,
                    usuario_id INTEGER NULL,
                    produto_id INT NOT NULL,
                    CONSTRAINT tb_movimentacoes_estoque_usuario_id_fk 
                        FOREIGN KEY (usuario_id) REFERENCES auth_user (id),
                    CONSTRAINT tb_movimentacoes_estoque_produto_id_fk 
                        FOREIGN KEY (produto_id) REFERENCES tb_produtos (id)
                )
            """)
            print("✓ Tabela 'tb_movimentacoes_estoque' criada com sucesso!")
            
            # Criar índices
            print("Criando índices...")
            cursor.execute("""
                CREATE INDEX tb_moviment_produto_idx 
                ON tb_movimentacoes_estoque (produto_id, data_movimentacao DESC)
            """)
            print("✓ Índices criados com sucesso!")
        else:
            print("✓ Tabela 'tb_movimentacoes_estoque' já existe.")
        
        # Verificar se o índice em qtd_estoque existe
        cursor.execute("""
            SELECT INDEX_NAME 
            FROM INFORMATION_SCHEMA.STATISTICS 
            WHERE TABLE_SCHEMA = 'BDVENDAS' 
            AND TABLE_NAME = 'tb_produtos' 
            AND COLUMN_NAME = 'qtd_estoque'
        """)
        
        if not cursor.fetchone():
            print("Criando índice em 'qtd_estoque'...")
            cursor.execute("""
                CREATE INDEX tb_produtos_qtd_est_idx ON tb_produtos (qtd_estoque)
            """)
            print("✓ Índice criado com sucesso!")
        else:
            print("✓ Índice em 'qtd_estoque' já existe.")
    
    print("\n✅ Banco de dados atualizado com sucesso!")

if __name__ == '__main__':
    try:
        check_and_update_schema()
    except Exception as e:
        print(f"\n❌ Erro ao atualizar banco de dados: {e}")
        import traceback
        traceback.print_exc()
