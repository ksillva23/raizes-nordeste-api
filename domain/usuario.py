from enum import Enum
from pydantic import BaseModel


class PerfilUsuarioEnum(str, Enum):
    ADMIN = "ADMIN"
    ATENDENTE = "ATENDENTE"


class Usuario(BaseModel):
    id: int | None = None
    nome: str
    email: str
    senhaHash: str
    perfil: PerfilUsuarioEnum
    ativo: bool = True