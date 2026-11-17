from typing import Optional
from infrastructure.database import get_connection
from domain.pedido import Pedido, ItemPedido, StatusPedidoEnum


class PedidoRepository:
    def salvar(self, pedido: Pedido) -> Pedido:
        conn = get_connection()
        cursor = conn.cursor()

        try:
            status_valor = pedido.status.value if hasattr(pedido.status, "value") else pedido.status
            canal_valor = pedido.canalPedido.value if hasattr(pedido.canalPedido, "value") else pedido.canalPedido
            pagamento_valor = pedido.formaPagamento.value if hasattr(pedido.formaPagamento, "value") else pedido.formaPagamento

            if not pedido.id or pedido.id == 0:
                cursor.execute("""
                    INSERT INTO pedidos (
                        unidade_id,
                        canal_pedido,
                        forma_pagamento,
                        status,
                        total
                    )
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    pedido.unidadeId,
                    canal_valor,
                    pagamento_valor,
                    status_valor,
                    pedido.total,
                ))
                pedido.id = cursor.lastrowid
            else:
                cursor.execute("""
                    UPDATE pedidos
                    SET unidade_id = ?,
                        canal_pedido = ?,
                        forma_pagamento = ?,
                        status = ?,
                        total = ?
                    WHERE id = ?
                """, (
                    pedido.unidadeId,
                    canal_valor,
                    pagamento_valor,
                    status_valor,
                    pedido.total,
                    pedido.id,
                ))
                cursor.execute("DELETE FROM itens_pedido WHERE pedido_id = ?", (pedido.id,))

            for item in pedido.itens:
                cursor.execute("""
                    INSERT INTO itens_pedido (
                        pedido_id,
                        produto_id,
                        quantidade,
                        preco_unitario
                    )
                    VALUES (?, ?, ?, ?)
                """, (
                    pedido.id,
                    item.produtoId,
                    item.quantidade,
                    item.precoUnitario,
                ))

            conn.commit()
            return pedido
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def buscar_por_id(self, pedido_id: int) -> Optional[Pedido]:
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM pedidos WHERE id = ?", (pedido_id,))
            row_pedido = cursor.fetchone()

            if not row_pedido:
                return None

            cursor.execute("SELECT * FROM itens_pedido WHERE pedido_id = ?", (pedido_id,))
            rows_itens = cursor.fetchall()

            itens = [
                ItemPedido(
                    produtoId=row["produto_id"],
                    quantidade=row["quantidade"],
                    precoUnitario=row["preco_unitario"],
                )
                for row in rows_itens
            ]

            return Pedido(
                id=row_pedido["id"],
                unidadeId=row_pedido["unidade_id"],
                canalPedido=row_pedido["canal_pedido"],
                formaPagamento=row_pedido["forma_pagamento"],
                status=StatusPedidoEnum(row_pedido["status"]),
                total=row_pedido["total"],
                itens=itens,
            )
        finally:
            conn.close()


repositorio_pedidos = PedidoRepository()
