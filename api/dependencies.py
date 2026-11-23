import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from infrastructure.usuario_repository import repositorio_usuarios

from application.jwt_service import JWTService


security = HTTPBearer()
jwt_service = JWTService()


def get_usuario_atual(
    credenciais: HTTPAuthorizationCredentials = Depends(security)
):
    token = credenciais.credentials

    try:
        payload = jwt_service.validar_token(token)

        usuario_id = payload.get("sub")

        if not usuario_id:
            raise HTTPException(
                status_code=401,
                detail="Token inválido."
            )

        usuario = repositorio_usuarios.buscar_por_id(
            int(usuario_id)
        )

        if not usuario or not usuario.ativo:
            raise HTTPException(
                status_code=401,
                detail="Usuário inexistente ou inativo."
            )

        return {
            "id": usuario.id,
            "perfil": usuario.perfil.value
        }

    except (jwt.InvalidTokenError, ValueError):
        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"}
        )

def exigir_admin(
    usuario: dict = Depends(get_usuario_atual)
):
    if usuario["perfil"] != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso permitido somente para administradores."
        )

    return usuario
