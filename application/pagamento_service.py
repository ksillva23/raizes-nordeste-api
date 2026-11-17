from infrastructure.database import get_connection
from domain.pedido import Pedido, StatusPagamentoEnum


class PagamentoMockService:
    @staticmethod
    def processar_pagamento(pedido: Pedido) -> dict:
        metodo_valor = (
            pedido.formaPagamento.value
            if hasattr(pedido.formaPagamento, "value")
            else pedido.formaPagamento
        )

        if metodo_valor.upper() == "RECUSAR":
            status_pgto = StatusPagamentoEnum.RECUSADO
        else:
            status_pgto = StatusPagamentoEnum.APROVADO

        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO pagamentos (
                    pedido_id,
                    metodo,
                    status,
                    valor
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    pedido.id,
                    metodo_valor,
                    status_pgto.value,
                    pedido.total,
                ),
            )
            pagamento_id = cursor.lastrowid
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

        pedido.atualizar_status_por_pagamento(status_pgto)

        return {
            "pagamentoId": pagamento_id,
            "pedidoId": pedido.id,
            "metodo": metodo_valor,
            "valor": pedido.total,
            "statusPagamento": status_pgto,
        }