import sqlite3

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.dependencies import exigir_admin
from application.auth_service import AuthService
from domain.usuario import Usuario, PerfilUsuarioEnum
from infrastructure.usuario_repository import repositorio_usuarios
from infrastructure.database import get_connection
from infrastructure.auditoria_repository import repositorio_auditoria


router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


class UsuarioRequest(BaseModel):
    nome: str
    email: str
    senha: str
    perfil: PerfilUsuarioEnum


@router.post("", status_code=201)
def cadastrar_usuario(
    dados: UsuarioRequest,
    administrador: dict = Depends(exigir_admin)
):
    auth_service = AuthService()

    usuario = Usuario(
        nome=dados.nome,
        email=dados.email,
        senhaHash=auth_service.gerar_hash(dados.senha),
        perfil=dados.perfil
    )

    conn = get_connection()

    try:
        usuario_salvo = repositorio_usuarios.salvar(
            usuario,
            conn
        )

        repositorio_auditoria.registrar(
            usuario_id=administrador["id"],
            acao="CADASTRAR",
            entidade="USUARIO",
            entidade_id=usuario_salvo.id,
            detalhes=f"Usuário cadastrado com perfil {usuario_salvo.perfil.value}",
            conn=conn
        )

        conn.commit()

        return {
            "mensagem": "Usuário cadastrado com sucesso.",
            "usuario": {
                "id": usuario_salvo.id,
                "nome": usuario_salvo.nome,
                "email": usuario_salvo.email,
                "perfil": usuario_salvo.perfil.value
            }
        }

    except sqlite3.IntegrityError:
        conn.rollback()

        raise HTTPException(
            status_code=409,
            detail="Já existe um usuário cadastrado com esse e-mail."
        )

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()