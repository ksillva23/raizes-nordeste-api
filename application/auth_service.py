from pwdlib import PasswordHash

from infrastructure.usuario_repository import repositorio_usuarios
from application.jwt_service import JWTService


class AuthService:

    def __init__(self):
        self.password_hash = PasswordHash.recommended()
        self.jwt_service = JWTService()

    def gerar_hash(self, senha: str) -> str:
        return self.password_hash.hash(senha)

    def verificar_senha(self, senha: str, senha_hash: str) -> bool:
        return self.password_hash.verify(senha, senha_hash)

    def autenticar(self, email: str, senha: str):

        usuario = repositorio_usuarios.buscar_por_email(email)

        if not usuario:
            return None

        if not usuario.ativo:
            return None

        senha_valida = self.verificar_senha(
            senha,
            usuario.senhaHash
        )

        if not senha_valida:
            return None

        token = self.jwt_service.gerar_token(
            usuario_id=usuario.id,
            perfil=usuario.perfil.value
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "usuario": {
                "id": usuario.id,
                "nome": usuario.nome,
                "email": usuario.email,
                "perfil": usuario.perfil.value
            }
        }