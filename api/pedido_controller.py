from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict, List
from domain.pedido import CanalEnum, ItemPedido, Pedido, StatusPedidoEnum
from application.pagamento_service import PagamentoMockService
from infrastructure.pedido_repository import repositorio_pedidos
from infrastructure.estoque_repository import repositorio_estoque
from infrastructure.database import get_connection
from api.dependencies import get_usuario_atual
from infrastructure.auditoria_repository import repositorio_auditoria

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"],
    dependencies=[Depends(get_usuario_atual)]
)


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
def criar_pedido(
    dados: PedidoRequest,
    usuario: dict = Depends(get_usuario_atual),
):
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
            (dados.unidadeId,),
        )

        if not cursor.fetchone():
            raise HTTPException(
                status_code=404,
                detail=f"Unidade {dados.unidadeId} não encontrada.",
            )

        for produto_id, quantidade_total in quantidades_agrupadas.items():
            cursor.execute(
                """
                SELECT id, preco_base
                FROM produtos
                WHERE id = ?
                """,
                (produto_id,),
            )

            row_produto = cursor.fetchone()

            if not row_produto:
                raise HTTPException(
                    status_code=404,
                    detail=f"Produto {produto_id} não encontrado.",
                )

            itens_dominio.append(
                ItemPedido(
                    produtoId=row_produto["id"],
                    quantidade=quantidade_total,
                    precoUnitario=row_produto["preco_base"],
                )
            )

        for produto_id, quantidade_total in quantidades_agrupadas.items():
            sucesso = repositorio_estoque.abater_estoque(
                dados.unidadeId,
                produto_id,
                quantidade_total,
                conn,
            )

            if not sucesso:
                raise HTTPException(
                    status_code=409,
                    detail=f"Não foi possível atualizar o estoque do produto {produto_id}.",
                )

        novo_pedido = Pedido(
            id=0,
            unidadeId=dados.unidadeId,
            itens=itens_dominio,
            canalPedido=dados.canalPedido,
            formaPagamento=dados.formaPagamento,
        )

        novo_pedido.calcular_total()

        pedido_salvo = repositorio_pedidos.salvar(novo_pedido, conn)
        resultado_pagamento = PagamentoMockService.processar_pagamento(
            pedido_salvo, conn
        )

        if resultado_pagamento["statusPagamento"].value == "RECUSADO":
            
            for produto_id, quantidade_total in quantidades_agrupadas.items():
                sucesso = repositorio_estoque.devolver_estoque(
                    dados.unidadeId,
                    produto_id,
                    quantidade_total,
                    conn,
                )

                if not sucesso:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Erro ao devolver estoque do produto {produto_id}.",
                    )

        repositorio_pedidos.salvar(pedido_salvo, conn)

        repositorio_auditoria.registrar(
            usuario_id=usuario["id"],
            acao="CRIAR",
            entidade="PEDIDO",
            entidade_id=pedido_salvo.id,
            detalhes=f"Pedido criado pelo canal {dados.canalPedido.value}",
            conn=conn,
        )

        conn.commit()
        return {
            "mensagem": "Pedido Registrado com Sucesso!",
            "pedido": pedido_salvo,
            "pagamento": resultado_pagamento,
        }
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


@router.get("/{pedido_id}")
def consultar_pedido(pedido_id: int):
    pedido = repositorio_pedidos.buscar_por_id(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não foi locaizado.")
    return pedido


@router.patch("/{pedido_id}/status")
def atualizar_status_pedido(
    pedido_id: int,
    dados: AtualizarStatusRequest,
    usuario: dict = Depends(get_usuario_atual),
):
    pedido = repositorio_pedidos.buscar_por_id(pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não foi locaizado.")

    status_anterior = pedido.status.value

    sucesso = pedido.avancar_status(dados.novoStatus)
    if not sucesso:
        raise HTTPException(
            status_code=400,
            detail=f"Transição inválida de '{pedido.status}' para '{dados.novoStatus}'.",
        )

    conn = get_connection()
    try:
        repositorio_pedidos.salvar(pedido, conn)

        repositorio_auditoria.registrar(
            usuario_id=usuario["id"],
            acao="ATUALIZAR_STATUS",
            entidade="PEDIDO",
            entidade_id=pedido.id,
            detalhes=(
                f"Status alterado de {status_anterior} "
                f"para {pedido.status.value}"
            ),
            conn=conn,
        )

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    return {"mensagem": "Status atualizado com sucesso.", "pedido": pedido}