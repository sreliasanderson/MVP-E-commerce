import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'logistica.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tabelas_frete (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            regiao TEXT NOT NULL,
            valor_base REAL NOT NULL
        )
    ''')
    # Insere dados mockados se a tabela estiver vazia
    if conn.execute('SELECT COUNT(*) FROM tabelas_frete').fetchone()[0] == 0:
        conn.execute("INSERT INTO tabelas_frete (regiao, valor_base) VALUES ('Sul', 20.0)")
        conn.execute("INSERT INTO tabelas_frete (regiao, valor_base) VALUES ('Sudeste', 15.0)")
    conn.commit()
    conn.close()