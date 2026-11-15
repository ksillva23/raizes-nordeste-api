from typing import Dict, Optional
from domain.pedido import Pedido

class PedidoRepository:
    def __init__(self):
        self._pedidos: Dict[int, Pedido] = {}
        self._contador_id = 1

    def salvar(self, pedido: Pedido) -> Pedido:
        if pedido.id == 0:
            self._contador_id += 1
            pedido.id = self._contador_id
        self._pedidos[pedido.id] = pedido
        return pedido

    def buscar_por_id(self, pedido_id: int) -> Optional[Pedido]:
        return self._pedidos.get(pedido_id)

repositorio_pedidos = PedidoRepository()
