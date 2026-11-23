# Rede Raízes do Nordeste — API Back-End

## 1. Sobre o projeto

O projeto **Rede Raízes do Nordeste** consiste no desenvolvimento de uma API REST para gerenciamento de pedidos e estoque de uma rede de franquias do ramo alimentício.

A solução foi desenvolvida como projeto acadêmico do curso de Análise e Desenvolvimento de Sistemas, com o objetivo de implementar funcionalidades relacionadas ao gerenciamento de pedidos, controle de estoque, autenticação de usuários e processamento simulado de pagamentos.

A API contempla diferentes canais de realização de pedidos, como aplicativo, totem, balcão, retirada e web.

## 2. Tecnologias utilizadas

- **Python 3:** linguagem de programação.
- **FastAPI:** desenvolvimento da API REST.
- **SQLite:** banco de dados relacional.
- **Pydantic:** validação e estruturação dos dados.
- **PyJWT:** geração e validação de tokens JWT.
- **pwdlib / Argon2:** criptografia e verificação de senhas.
- **python-dotenv:** gerenciamento de variáveis de ambiente.
- **Uvicorn:** servidor ASGI para execução da aplicação.
- **Postman:** realização dos testes dos endpoints.

## 3. Arquitetura do projeto

O projeto utiliza uma organização em camadas, buscando separar as responsabilidades e facilitar a manutenção do código.

```text
projetoFinal-raizes-nordeste/
│
├── api/
│   ├── auth_controller.py
│   ├── dependencies.py
│   ├── pedido_controller.py
│   └── usuario_controller.py
│
├── application/
│   ├── auth_service.py
│   ├── jwt_service.py
│   └── pagamento_service.py
│
├── domain/
│   └── pedido.py
│
├── infrastructure/
│   ├── database.py
│   ├── estoque_repository.py
│   └── pedido_repository.py
│
├── main.py
├── requirements.txt
├── .env.example
└── .gitignore
```

### Responsabilidades das camadas

- **API:** disponibiliza os endpoints, recebe requisições e controla o acesso às funcionalidades.
- **Application:** concentra os serviços e as regras de aplicação, como autenticação e processamento de pagamentos.
- **Domain:** representa as entidades, enumerações e regras centrais do domínio.
- **Infrastructure:** realiza a comunicação com o banco de dados e implementa a persistência das informações.

## 4. Funcionalidades implementadas

### Autenticação e usuários

- Autenticação de usuários por e-mail e senha.
- Geração de tokens JWT.
- Armazenamento de senhas utilizando hash seguro.
- Controle de acesso por perfil de usuário.
- Cadastro de usuários com permissão administrativa.

### Gerenciamento de pedidos

- Criação de pedidos.
- Consulta de pedidos cadastrados.
- Identificação do canal de realização do pedido.
- Associação de produtos, quantidades e valores.
- Atualização do status dos pedidos.
- Validação das transições de status.

### Controle de estoque

- Consulta da disponibilidade dos produtos.
- Verificação de estoque antes da criação do pedido.
- Baixa automática do estoque após a criação do pedido.
- Devolução do estoque quando o pagamento simulado é recusado.

### Pagamento simulado

O projeto possui um serviço de pagamento simulado, permitindo representar dois cenários:

- **Aprovado:** o pedido avança para o status `EM_PREPARO`.
- **Recusado:** o pedido permanece em `AGUARDANDO_PAGAMENTO`, e o estoque é restaurado.

O serviço não realiza transações financeiras reais.

### Auditoria

O sistema registra ações relevantes realizadas pelos usuários, incluindo operações relacionadas à criação de usuários e à atualização de status dos pedidos.

## 5. Banco de dados

A aplicação utiliza SQLite para persistência dos dados.

Entre as principais tabelas estão:

- `unidades`
- `produtos`
- `estoque`
- `pedidos`
- `itens_pedido`
- `pagamentos`
- `usuarios`
- `logs_auditoria`

A estrutura do banco de dados é inicializada pela aplicação durante sua inicialização, por meio da função `initialize_database()`.

## 6. Requisitos para execução

Antes de executar o projeto, é necessário possuir:

- Python 3 instalado.
- Pip para gerenciamento