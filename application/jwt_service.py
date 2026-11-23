import os
import jwt
from datetime import datetime, timedelta, timezone


class JWTService:

    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY")

        if not self.secret_key:
            raise ValueError("SECRET_KEY não configurada.")

        self.algorithm = "HS256"

    def gerar_token(self, usuario_id: int, perfil: str) -> str:

        agora = datetime.now(timezone.utc)

        payload = {
            "sub": str(usuario_id),
            "perfil": perfil,
            "iat": agora,
            "exp": agora + timedelta(hours=2)
        }

        token = jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm
        )

        return token

    def validar_token(self, token: str) -> dict:

        payload = jwt.decode(
            token,
            self.secret_key,
            algorithms=[self.algorithm]
        )

        return payload

if __name__ == "__main__":

    jwt_service = JWTService()

    token = jwt_service.gerar_token(
        usuario_id=1,
        perfil="ADMIN"
    )

    print("Token gerado:", token)

    dados = jwt_service.validar_token(token)

    print("Dados do token:", dados)