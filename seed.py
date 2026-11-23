
from infrastructure.database import get_connection, initialize_database


def executar_seed():
    initialize_database()
    conn = get_connection()

    try:
        cursor = conn.cursor()

        unidades = [
            (1, "Unidade Centro", "Rua Principal, 100"),
            (2, "Unidade Bairro", "Avenida Nordeste, 200"),
        ]

        produtos = [
            (10, "Baião de Dois", "Prato típico nordestino", 28.90),
            (20, "Carne de Sol com Mandioca",
             "Carne de sol acompanhada de mandioca", 35.90),
            (30, "Cuscuz Recheado", "Cuscuz com recheio especial", 22.90),
        ]

        estoques = [
            (1, 10, 12),
            (1, 20, 7),
            (1, 30, 20),
            (2, 10, 12),
            (2, 20, 10),
            (2, 30, 15),
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO unidades (id, nome, endereco)
            VALUES (?, ?, ?)
        """, unidades)

        cursor.executemany("""
            INSERT OR IGNORE INTO produtos
                (id, nome, descricao, preco_base)
            VALUES (?, ?, ?, ?)
        """, produtos)

        cursor.executemany("""
            INSERT OR IGNORE INTO estoque
                (unidade_id, produto_id, quantidade)
            VALUES (?, ?, ?)
        """, estoques)

        conn.commit()
        print("Dados iniciais cadastrados com sucesso!")

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    executar_seed()
