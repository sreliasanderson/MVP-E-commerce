import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'ecommerce.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL,
            cep_destino TEXT NOT NULL,
            endereco_completo TEXT,
            valor_frete REAL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()