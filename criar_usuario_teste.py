from getpass import getpass
from pwdlib import PasswordHash

from domain.usuario import Usuario, PerfilUsuarioEnum
from infrastructure.usuario_repository import repositorio_usuarios


nome = input("Nome do administrador: ")
email = input("E-mail: ")
senha = getpass("Senha: ")

password_hash = PasswordHash.recommended()

usuario = Usuario(
    nome=nome,
    email=email,
    senhaHash=password_hash.hash(senha),
    perfil=PerfilUsuarioEnum.ADMIN
)

usuario_salvo = repositorio_usuarios.salvar(usuario)

print(f"\nUsuário cadastrado com sucesso! ID: {usuario_salvo.id}")