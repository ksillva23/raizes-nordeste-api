class AuditoriaRepository:

    def registrar(
        self,
        usuario_id: int,
        acao: str,
        entidade: str,
        entidade_id: int,
        detalhes: str,
        conn
    ):
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO logs_auditoria (
                usuario_id,
                acao,
                entidade,
                entidade_id,
                detalhes
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                usuario_id,
                acao,
                entidade,
                entidade_id,
                detalhes
            )
        )


repositorio_auditoria = AuditoriaRepository()