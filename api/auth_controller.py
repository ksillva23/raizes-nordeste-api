from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from application.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)

auth_service = AuthService()


class LoginRequest(BaseModel):
    email: str
    senha: str


@router.post("/login")
def login(dados: LoginRequest):

    resultado = auth_service.autenticar(
        email=dados.email,
        senha=dados.senha
    )

    if not resultado:
        raise HTTPException(
            status_code=401,
            detail="E-mail ou senha inválidos."
        )

    return resultado
