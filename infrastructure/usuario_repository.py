from typing import Optional
from infrastructure.database import get_connection
from domain.usuario import Usuario, PerfilUsuarioEnum


class UsuarioRepository:
    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT id, nome, email, senha_hash, perfil, ativo
                FROM usuarios
                WHERE email = ?
                """,
                (email,),
            )
            row = cursor.fetchone()

            if not row:
                return None

            return Usuario(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                senhaHash=row["senha_hash"],
                perfil=PerfilUsuarioEnum(row["perfil"]),
                ativo=bool(row["ativo"]),
            )
        finally:
            conn.close()

    def buscar_por_id(self, usuario_id: int) -> Optional[Usuario]:
        conn = get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                SELECT id, nome, email, senha_hash, perfil, ativo
                FROM usuarios
                WHERE id = ?
                """,
                (usuario_id,),
            )

            row = cursor.fetchone()

            if not row:
                return None

            return Usuario(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                senhaHash=row["senha_hash"],
                perfil=PerfilUsuarioEnum(row["perfil"]),
                ativo=bool(row["ativo"]),
            )
        finally:
            conn.close()

    def salvar(self, usuario: Usuario, conn=None) -> Usuario:
        propria_conexao = conn is None

        if propria_conexao:
            conn = get_connection()

        cursor = conn.cursor()

        try:
            perfil_valor = (
                usuario.perfil.value
                if hasattr(usuario.perfil, "value")
                else usuario.perfil
            )

            ativo_valor = 1 if usuario.ativo else 0

            if usuario.id is None:
                cursor.execute(
                    """
                    INSERT INTO usuarios (
                        nome, email, senha_hash, perfil, ativo
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        usuario.nome,
                        usuario.email,
                        usuario.senhaHash,
                        perfil_valor,
                        ativo_valor,
                    ),
                )

                usuario.id = cursor.lastrowid

            else:
                cursor.execute(
                    """
                    UPDATE usuarios
                    SET nome = ?,
                        email = ?,
                        senha_hash = ?,
                        perfil = ?,
                        ativo = ?
                    WHERE id = ?
                    """,
                    (
                        usuario.nome,
                        usuario.email,
                        usuario.senhaHash,
                        perfil_valor,
                        ativo_valor,
                        usuario.id,
                    ),
                )

            if propria_conexao:
                conn.commit()

            return usuario

        except Exception:
            if propria_conexao:
                conn.rollback()
            raise

        finally:
            if propria_conexao:
                conn.close()

repositorio_usuarios = UsuarioRepository()