from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from domain.pedido import CanalEnum, ItemPedido, Pedido, StatusPedidoEnum
from application.pagamento_service import PagamentoMockService
from infrastructure.pedido_repository import repositorio_pedidos
from infrastructure.estoque_repository import repositorio_estoque

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

class ItemPedidoRequest(BaseModel):
    produtoId: int
    quantidade: int

class PedidoRequest(BaseModel):
    unidadeId: int
    itens: List[ItemPedidoRequest]
    formaPagamento: str
    canalPedido: CanalEnum

class AtualizarStatusRequest(BaseModel):
    novoStatus: StatusPedidoEnum

@router.post("", status_code=201)
def criar_pedido(dados: PedidoRequest):
    for item in dados.itens:
        saldo = repositorio_estoque.consultar_saldo(dados.unidadeId, item.produtoId)
        if saldo < item.quantidade:
            raise HTTPException(
                status_code=400,
                detail=f"Estoque insuficiente na unidade {dados.unidadeId} para o produto {item.produtoId}. Saldo: {saldo}."
            )

    for item in dados.itens:
        repositorio_estoque.abater_estoque(dados.unidadeId, item.produtoId, item.quantidade)

    itens_dominio = [
        ItemPedido(produtoId=item.produtoId, quantidade=item.quantidade)
        for item in dados.itens
    ]
    novo_pedido = Pedido(
        id=0,
        unidadeId=dados.unidadeId,
        itens=itens_dominio,
        canalPedido=dados.canalPedido,
        formaPagamento=dados.formaPagamento
    )
    novo_pedido.calcular_total()

    pedido_salvo = repositorio_pedidos.salvar(novo_pedido)
    resultado_pagamento = PagamentoMockService.processar_pagamento(pedido_salvo)
    repositorio_pedidos.salvar(pedido_salvo)

    return {
        "mensagem": "Pedido Registrado com Sucesso!",
        "pedido": pedido_salvo,
        "pagamento": resultado_pagamento
    }

@router.get("/{pedido_id}")
def consultar_pedido(pedido_id: int):
    pedido = repositorio_pedidos.buscar_por_id(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não foi locaizado.")
    return pedido

@router.patch("/{pedido_id}/status")
def atualizar_status_pedido(pedido_id: int, dados: AtualizarStatusRequest):
    pedido = repositorio_pedidos.buscar_por_id(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não foi locaizado.")
    
    sucesso = pedido.avancar_status(dados.novoStatus)
    if not sucesso:
        raise HTTPException(
            status_code=400,
            detail=f"Transição inválida de '{pedido.status}' para '{dados.novoStatus}'."
        )
    
    repositorio_pedidos.salvar(pedido)
    return {"mensagem": "Status atualizado com sucesso.", "pedido": pedido}