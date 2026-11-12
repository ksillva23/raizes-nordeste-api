from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from enum import Enum

app = FastAPI(
    title="API - Raízes do Nordeste",
    description="API feita para Gestão de Pedidos, Stock e Pagamentos Multicanal.",
    version="1.0.0"
)

# --- 1. MODELOS DE VALIDAÇÃO (CONTRATOS) ---

class CanalEnum(str, Enum):
    APP = "APP"
    TOTEM = "TOTEM"
    BALCAO = "BALCAO"
    PICKUP = "PICKUP"
    WEB = "WEB"

class ItemPedidoRequest(BaseModel):
    produtoId: int
    quantidade: int

class PedidoRequest(BaseModel):
    unidadeId: int
    itens: List[ItemPedidoRequest]
    formaPagamento: str
    canalPedido: CanalEnum

# --- 2. ROTAS (ENDPOINTS) ---

@app.get("/")
def health_check():
    return {"status": "A API está a funcionar perfeitamente!"}

@app.post("/pedidos", status_code=201, tags=["Pedidos"])
def criar_pedido(pedido: PedidoRequest):
    return {
        "pedidoId": 9001,
        "status": "AGUARDANDO_PAGAMENTO",
        "total_calculado": 0.00,
        "dados_recebidos": pedido
    }