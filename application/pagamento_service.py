from domain.pedido import Pedido, StatusPagamentoEnum

class PagamentoMockService:
    @staticmethod
    def processar_pagamento(pedido: Pedido) -> dict:
        if pedido.formaPagamento.upper() == "RECUSAR":
            status_pgto = StatusPagamentoEnum.RECUSADO
        else:
            status_pgto = StatusPagamentoEnum.APROVADO
            
        pedido.atualizar_status_por_pagamento(status_pgto)

        return {
            "pagamentoId": pedido.id + 500,
            "pedidoId": pedido.id,
            "metodo": pedido.formaPagamento,
            "statusPagamento": status_pgto
        }