import sqlite3


conn = sqlite3.connect("banco.db")
cursor = conn.cursor()

def tabela_pessoas():

    cursor.execute("""CREATE TABLE IF NOT EXISTS pessoas
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    embedding TEXT)
    """)

def tabela_acessos():
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS acessos
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        pessoa_id INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        resultado TEXT CHECK(resultado IN('reconhecido', 'desconhecido')),
        foto_path TEXT,
        FOREIGN KEY (pessoa_id) REFERENCES pessoas(id))
        """)

tabela_pessoas()
tabela_acessos()

conn.commit()
conn.close()