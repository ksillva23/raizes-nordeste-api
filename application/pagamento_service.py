
from domain.pedido import Pedido, StatusPagamentoEnum


class PagamentoMockService:
    @staticmethod
    def processar_pagamento(pedido: Pedido, conn) -> dict:
        metodo_valor = (
            pedido.formaPagamento.value
            if hasattr(pedido.formaPagamento, "value")
            else pedido.formaPagamento
        )

        if metodo_valor.upper() == "RECUSAR":
            status_pgto = StatusPagamentoEnum.RECUSADO
        else:
            status_pgto = StatusPagamentoEnum.APROVADO

        cursor = conn.cursor()

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

        pedido.atualizar_status_por_pagamento(status_pgto)

        return {
            "pagamentoId": pagamento_id,
            "pedidoId": pedido.id,
            "metodo": metodo_valor,
            "valor": pedido.total,
            "statusPagamento": status_pgto,
        }
