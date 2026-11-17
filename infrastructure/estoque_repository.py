from infrastructure.database import get_connection


class EstoqueRepository:
    def consultar_saldo(self, unidade_id: int, produto_id: int) -> int:
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT quantidade
                FROM estoque
                WHERE unidade_id = ? AND produto_id = ?
                """,
                (unidade_id, produto_id),
            )
            row = cursor.fetchone()
            return row["quantidade"] if row else 0
        finally:
            conn.close()

    def abater_estoque(self, unidade_id: int, produto_id: int, quantidade: int) -> bool:
        if quantidade <= 0:
            return False

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                UPDATE estoque
                SET quantidade = quantidade - ?
                WHERE unidade_id = ?
                  AND produto_id = ?
                  AND quantidade >= ?
                """,
                (quantidade, unidade_id, produto_id, quantidade),
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def repor_estoque(self, unidade_id: int, produto_id: int, quantidade: int) -> bool:
        if quantidade <= 0:
            return False

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                UPDATE estoque
                SET quantidade = quantidade + ?
                WHERE unidade_id = ? AND produto_id = ?
                """,
                (quantidade, unidade_id, produto_id),
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()


repositorio_estoque = EstoqueRepository()