from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from domain.pedido import CanalEnum, ItemPedido, Pedido, StatusPedidoEnum
from application.pagamento_service import PagamentoMockService
from infrastructure.pedido_repository import repositorio_pedidos
from infrastructure.estoque_repository import repositorio_estoque
from infrastructure.database import get_connection

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
    if not dados.itens:
        raise HTTPException(
            status_code=400,
            detail="O pedido deve conter pelo menos um item.",
        )

    quantidades_agrupadas: Dict[int, int] = {}

    for item in dados.itens:
        if item.quantidade <= 0:
            raise HTTPException(
                status_code=400,
                detail=f"Quantidade inválida para o produto {item.produtoId}. Deve ser maior que zero.",
            )

        quantidades_agrupadas[item.produtoId] = (
            quantidades_agrupadas.get(item.produtoId, 0) + item.quantidade
        )

    itens_dominio: List[ItemPedido] = []
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT id FROM unidades WHERE id = ?",
            (dados.unidadeId,)
        )

        if not cursor.fetchone():
            raise HTTPException(
                status_code=404,
                detail=f"Unidade {dados.unidadeId} não encontrada."
            )

        for produto_id, quantidade_total in quantidades_agrupadas.items():
            cursor.execute(
                """
                SELECT id, preco_base
                FROM produtos
                WHERE id = ?
                """,
                (produto_id,)
            )

            row_produto = cursor.fetchone()

            if not row_produto:
                raise HTTPException(
                    status_code=404,
                    detail=f"Produto {produto_id} não encontrado."
                )

            itens_dominio.append(
                ItemPedido(
                    produtoId=row_produto["id"],
                    quantidade=quantidade_total,
                    precoUnitario=row_produto["preco_base"],
                )
            )

    finally:
        conn.close()

    for produto_id, quantidade_total in quantidades_agrupadas.items():
        saldo = repositorio_estoque.consultar_saldo(
            dados.unidadeId, produto_id
        )

        if saldo < quantidade_total:
            raise HTTPException(
                status_code=409,
                detail=f"Estoque insuficiente na unidade {dados.unidadeId} para o produto {produto_id}. Saldo: {saldo}.",
            )

    for produto_id, quantidade_total in quantidades_agrupadas.items():
        sucesso = repositorio_estoque.abater_estoque(
            dados.unidadeId,
            produto_id,
            quantidade_total
        )

        if not sucesso:
            raise HTTPException(
                status_code=409,
                detail=f"Não foi possível atualizar o estoque do produto {produto_id}."
            )

    novo_pedido = Pedido(
        id=0,
        unidadeId=dados.unidadeId,
        itens=itens_dominio,
        canalPedido=dados.canalPedido,
        formaPagamento=dados.formaPagamento,
    )

    novo_pedido.calcular_total()

    pedido_salvo = repositorio_pedidos.salvar(novo_pedido)
    resultado_pagamento = PagamentoMockService.processar_pagamento(pedido_salvo)
    repositorio_pedidos.salvar(pedido_salvo)

    return {
        "mensagem": "Pedido Registrado com Sucesso!",
        "pedido": pedido_salvo,
        "pagamento": resultado_pagamento,
    }
