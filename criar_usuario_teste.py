
from getpass import getpass
from pwdlib import PasswordHash

from domain.usuario import Usuario, PerfilUsuarioEnum
from infrastructure.usuario_repository import repositorio_usuarios


nome = input("Nome do administrador: ").strip()
email = input("E-mail: ").strip().lower()

if repositorio_usuarios.buscar_por_email(email):
    print("\nJá existe um usuário cadastrado com esse e-mail.")
else:
    senha = getpass("Senha: ")

    if not nome or not email or not senha:
        print("\nTodos os campos são obrigatórios.")
    else:
        password_hash = PasswordHash.recommended()

        usuario = Usuario(
            nome=nome,
            email=email,
            senhaHash=password_hash.hash(senha),
            perfil=PerfilUsuarioEnum.ADMIN
        )

        usuario_salvo = repositorio_usuarios.salvar(usuario)

        print(
            f"\nAdministrador cadastrado com sucesso! "
            f"ID: {usuario_salvo.id}"
        )
