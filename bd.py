import sqlite3

def iniciar_bd():
    conn = sqlite3.connect('orcamento.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS Despesas (
            id INTEGER PRIMARY KEY,
            categoria TEXT,
            descricao TEXT,
            valor REAL,
            data TEXT
        )
    ''')
    conn.commit()
    conn.close()

iniciar_bd()
