from getpass import getpass
from application.auth_service import AuthService

auth = AuthService()

email = input("E-mail: ")
senha = getpass("Senha: ")

resultado = auth.autenticar(email, senha)

if resultado:
    print("\nLogin realizado com sucesso!")
    print("Usuário:", resultado["usuario"])
    print("Tipo de token:", resultado["token_type"])
    print("Token gerado:", bool(resultado["access_token"]))
else:
    print("\nE-mail ou senha inválidos.")

print("\n--- Testando senha incorreta ---")

resultado_invalido = auth.autenticar(
    email,
    "SenhaIncorreta123"
)

print("Autenticação rejeitada:", resultado_invalido is None)
