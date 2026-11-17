from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "raizes_nordeste.db"


def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS unidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            endereco TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT,
            preco_base REAL NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unidade_id INTEGER NOT NULL,
            produto_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL DEFAULT 0,
            UNIQUE(unidade_id, produto_id),
            FOREIGN KEY (unidade_id) REFERENCES unidades(id),
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unidade_id INTEGER NOT NULL,
            canal_pedido TEXT NOT NULL,
            forma_pagamento TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'AGUARDANDO_PAGAMENTO',
            total REAL NOT NULL DEFAULT 0,
            data_criacao TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (unidade_id) REFERENCES unidades(id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            produto_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pagamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            metodo TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'PENDENTE',
            valor REAL NOT NULL,
            data_criacao TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
        );
    """)

    conn.commit()
    conn.close()