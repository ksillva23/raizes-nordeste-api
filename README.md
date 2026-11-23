# Rede Raízes do Nordeste — API Back-End

## 1. Sobre o projeto

O projeto **Rede Raízes do Nordeste** consiste no desenvolvimento de uma API REST para gerenciamento de pedidos e estoque de uma rede de franquias do ramo alimentício.

Desenvolvido como projeto acadêmico do curso de Análise e Desenvolvimento de Sistemas, o sistema tem como objetivo implementar funcionalidades relacionadas ao gerenciamento de pedidos, controle de estoque, autenticação de usuários e processamento simulado de pagamentos.

A API contempla diferentes canais de realização de pedidos, como aplicativo, totem, balcão, retirada e web.

## 2. Tecnologias utilizadas

- **Python 3:** linguagem de programação.
- **FastAPI:** desenvolvimento da API REST.
- **SQLite:** banco de dados relacional.
- **Pydantic:** validação e estruturação dos dados.
- **PyJWT:** geração e validação de tokens JWT.
- **pwdlib / Argon2:** hash e verificação de senhas.
- **python-dotenv:** gerenciamento de variáveis de ambiente.
- **Uvicorn:** servidor ASGI para execução da aplicação.
- **Postman:** realização dos testes dos endpoints.

## 3. Arquitetura do projeto

O projeto utiliza uma organização em camadas, separando as responsabilidades para facilitar a manutenção e a organização do código.

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
│   ├── pedido.py
│   └── usuario.py
│
├── infrastructure/
│   ├── auditoria_repository.py
│   ├── database.py
│   ├── estoque_repository.py
│   ├── pedido_repository.py
│   └── usuario_repository.py
│
├── criar_usuario_teste.py
├── seed.py
├── testar_auth.py
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### Responsabilidades das camadas

- **API:** disponibiliza os endpoints, recebe requisições e controla o acesso às funcionalidades.
- **Application:** concentra os serviços e as regras de aplicação, como autenticação e processamento de pagamentos.
- **Domain:** representa as entidades, enumerações e regras centrais do domínio.
- **Infrastructure:** realiza a comunicação com o banco de dados e implementa a persistência das informações.

## 4. Funcionalidades implementadas

### 4.1. Autenticação e usuários

- Autenticação de usuários por e-mail e senha.
- Geração e validação de tokens JWT.
- Armazenamento de senhas utilizando hash seguro.
- Controle de acesso por perfil de usuário.
- Perfis ADMIN e ATENDENTE.
- Cadastro de usuários com permissão administrativa.

### 4.2. Gerenciamento de pedidos

- Criação de pedidos.
- Consulta de pedidos cadastrados.
- Identificação do canal de realização do pedido.
- Associação de produtos, quantidades e valores.
- Atualização do status dos pedidos.
- Validação das transições de status.

### 4.3. Controle de estoque

- Consulta da disponibilidade dos produtos.
- Verificação do estoque antes da criação do pedido.
- Baixa automática do estoque após a criação do pedido.
- Devolução do estoque quando o pagamento simulado é recusado.

### 4.4. Pagamento simulado

O projeto possui um serviço de pagamento simulado, permitindo representar dois cenários:

- **Pagamento aprovado:** o pedido avança para o status `EM_PREPARO`.
- **Pagamento recusado:** o pedido permanece em `AGUARDANDO_PAGAMENTO`, e o estoque é restaurado.

O serviço não realiza transações financeiras reais.

### 4.5. Auditoria

O sistema registra ações relevantes realizadas pelos usuários, incluindo operações relacionadas ao cadastro de usuários e à atualização do status dos pedidos.

## 5. Banco de dados

A aplicação utiliza SQLite para persistência dos dados.

As principais tabelas são:

| Tabela | Descrição |
|---|---|
| `unidades` | Cadastro das unidades |
| `produtos` | Cadastro dos produtos |
| `estoque` | Quantidade de produtos por unidade |
| `pedidos` | Registro dos pedidos |
| `itens_pedido` | Produtos associados aos pedidos |
| `pagamentos` | Registro dos pagamentos |
| `usuarios` | Usuários e seus respectivos perfis |
| `logs_auditoria` | Histórico de ações relevantes |

A estrutura do banco de dados é criada automaticamente durante a inicialização da aplicação, por meio da função `initialize_database()`.

O arquivo SQLite utilizado é `raizes_nordeste.db`, localizado na raiz do projeto.

## 6. Requisitos para execução

Antes de executar o projeto, é necessário possuir:

- Python 3 instalado.
- Pip para gerenciamento de dependências.
- Git para clonar o repositório.

## 7. Instalação e configuração

### 7.1. Clonar o repositório

```bash
git clone https://github.com/ksillva23/raizes-nordeste-api.git
```

Acesse a pasta do projeto:

```bash
cd raizes-nordeste-api
```

### 7.2. Criar o ambiente virtual

```bash
python -m venv venv
```

Ative o ambiente virtual no Windows:

```powershell
venv\Scripts\activate
```

### 7.3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 7.4. Configurar as variáveis de ambiente

Na raiz do projeto, crie um arquivo chamado `.env`, utilizando o `.env.example` como referência.

Gere uma chave segura executando:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Configure o arquivo `.env`:

```env
SECRET_KEY=sua_chave_secreta
```

**Importante:** o arquivo `.env` contém informações sensíveis e não deve ser publicado no GitHub. O `.env.example` serve como modelo de configuração.

### 7.5. Preparar o banco de dados

Após instalar as dependências e configurar as variáveis de ambiente, execute:

```bash
python seed.py
```

Esse comando cria as tabelas necessárias e cadastra os dados iniciais de demonstração:

- Duas unidades.
- Três produtos.
- Seis registros de estoque.

O script utiliza inserções que evitam duplicar os registros iniciais quando executado novamente.

### 7.6. Criar o primeiro administrador

Para cadastrar o primeiro usuário administrador, execute:

```bash
python criar_usuario_teste.py
```

O programa solicitará:

- Nome do administrador.
- E-mail.
- Senha.

A senha será solicitada sem aparecer na tela e armazenada utilizando hash seguro.

O script também verifica se o e-mail já está cadastrado, evitando duplicidade.

## 8. Executando a aplicação

Com o ambiente virtual ativado, as dependências instaladas, o banco preparado e o administrador cadastrado, execute:

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8001
```

A API estará disponível em:

```text
http://127.0.0.1:8001
```

## 9. Documentação da API

A documentação interativa é disponibilizada pelo Swagger UI, gerado automaticamente pelo FastAPI.

Acesse:

http://127.0.0.1:8001/docs

Por meio do Swagger, é possível visualizar os endpoints, consultar parâmetros, enviar requisições e verificar as respostas da API.

## 10. Principais endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/` | Verificação de funcionamento da API |
| POST | `/auth/login` | Autenticação de usuário |
| POST | `/usuarios` | Cadastro de usuário |
| POST | `/pedidos` | Criação de pedido |
| GET | `/pedidos/{pedido_id}` | Consulta de pedido |
| PATCH | `/pedidos/{pedido_id}/status` | Atualização do status do pedido |

Os endpoints protegidos exigem autenticação por token JWT, conforme as permissões configuradas na aplicação.

## 11. Testes da API

Os testes foram realizados utilizando o Postman, contemplando cenários positivos e negativos.

Entre os cenários verificados estão:

- Login com credenciais válidas e inválidas.
- Cadastro de usuários com e sem autenticação.
- Controle de permissões entre ADMIN e ATENDENTE.
- Consulta de pedidos existentes e inexistentes.
- Criação de pedidos com pagamento aprovado e recusado.
- Tentativa de criação de pedido com estoque insuficiente.
- Validação de quantidade, produtos e unidades.
- Atualização de status com transições válidas e inválidas.
- Verificação de acesso a endpoints protegidos.
- Registro de ações de auditoria.

A coleção de testes do Postman deve acompanhar os materiais de entrega do projeto.

## 12. Segurança

Foram implementados mecanismos básicos de segurança, incluindo:

- Autenticação utilizando JWT.
- Controle de acesso baseado em perfis.
- Armazenamento de senhas por meio de hash.
- Proteção de endpoints que exigem autenticação.
- Registro de ações relevantes em logs de auditoria.
- Utilização de variáveis de ambiente para armazenamento da chave JWT.

## 13. Considerações finais

O projeto busca demonstrar a aplicação prática dos conceitos de desenvolvimento Back-End, arquitetura em camadas, persistência de dados, autenticação, autorização e integração entre serviços.

A implementação representa uma solução acadêmica para gerenciamento de pedidos e estoque da Rede Raízes do Nordeste, utilizando tecnologias e práticas aplicáveis ao desenvolvimento de APIs REST.