from enum import Enum
from typing import List
from pydantic import BaseModel

class CanalEnum(str, Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICKUP"
    WEB = "WEB"

class StatusPedidoEnum(str, Enum):
    AGUARDANDO_PAGAMENTO = "AGUARDANDO_PAGAMENTO"
    EM_PREPARO = "EM_PREPARO"
    PRONTO = "PRONTO"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"

class StatusPagamentoEnum(str, Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    RECUSADO = "RECUSADO"

class ItemPedido(BaseModel):
    produtoId: int
    quantidade: int
    precoUnitario: float = 30

    def calcular_subtotal(self) -> float:
        return self.quantidade * self.precoUnitario

class Pedido(BaseModel):
    id: int
    unidadeId: int
    itens: List[ItemPedido]
    canalPedido: CanalEnum
    formaPagamento: str
    status: StatusPedidoEnum = StatusPedidoEnum.AGUARDANDO_PAGAMENTO
    total: float = 0.0

    def calcular_total(self) -> float:
        self.total = sum(item.calcular_subtotal() for item in self.itens)
        return self.total

    def atualizar_status_por_pagamento(self, status_pagamento: StatusPagamentoEnum):
        if status_pagamento == StatusPagamentoEnum.APROVADO:
            self.status = StatusPedidoEnum.EM_PREPARO
        elif status_pagamento == StatusPagamentoEnum.RECUSADO:
            self.status = StatusPedidoEnum.CANCELADO

    def avancar_status(self, novo_status: StatusPedidoEnum) -> bool:
        transicoes_validas = {
            StatusPedidoEnum.EM_PREPARO: [StatusPedidoEnum.PRONTO, StatusPedidoEnum.CANCELADO],
            StatusPedidoEnum.PRONTO: [StatusPedidoEnum.ENTREGUE]
        }
        permitidos = transicoes_validas.get(self.status, [])
        if novo_status not in permitidos:
            return False
        self.status = novo_status
        return True