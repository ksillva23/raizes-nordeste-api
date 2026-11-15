from typing import Dict, Tuple

class EstoqueRepository:
    def __init__(self):
        #Achei interessante criar um catálogo para simular os produtos do Restaurante, segue: 10 = Baião de Dois, 20 = Carne de Sol com Mandioca, 30 = Cuscuz Recheado
        self._estoque: Dict[Tuple[int, int], int] = {
            (1, 10): 15,  
            (1, 20): 8,   
            (1, 30): 20,
            (2, 10): 12   
        }

    def consultar_saldo(self, unidade_id: int, produto_id: int) -> int:
        return self._estoque.get((unidade_id, produto_id), 0)

    def abater_estoque(self, unidade_id: int, produto_id: int, quantidade: int) -> bool:
        saldo_atual = self.consultar_saldo(unidade_id, produto_id)
        if saldo_atual < quantidade:
            return False
        self._estoque[(unidade_id, produto_id)] = saldo_atual - quantidade
        return True

repositorio_estoque = EstoqueRepository()