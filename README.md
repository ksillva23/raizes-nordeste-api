# API Back-End - Raízes do Nordeste

Este sistema foi desenvolvido com o objetivo de gerenciar pedidos multicanal, controlar o estoque por unidade e processar pagamentos da rede de restaurantes Raízes do Nordeste.

## Arquitetura do Projeto

O desenvolvimento do projeto foi estruturado em 4 camadas para fins de separação de responsabilidades:
- `domain/`: Possui as regras de negócio, entidades e validações de transição de status.
- `application/`: Casos de uso e simulação do serviço de pagamento integrado (Mock).
- `infrastructure/`: Possui repositórios em memória para armazenamento interno de pedidos e também controle de saldo de estoque.
- `api/`: Controladores REST e validação de contratos de entrada.

## Tecnologias Utilizadas
- Python 3
- FastAPI & Uvicorn
- Pydantic

## Como Executar Localmente

1. Clone o repositório e acesse a pasta do projeto.
2. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate

   ```
3. Instale as dependências necessárias:
   ```bash
   pip install fastapi uvicorn
   ```
4. Inicie o servidor da aplicação:
   ```bash
   uvicorn main:app --reload
   ```
5. Abra o navegador e acesse a documentação interativa (Swagger) em: `http://127.0.0.1:8000/docs`

## Endpoints Principais
- `POST /pedidos`: Cria um novo pedido, valida e abate o estoque da unidade e processa o pagamento.
- `GET /pedidos/{pedido_id}`: Consulta os detalhes e o status atual de um pedido.
- `PATCH /pedidos/{pedido_id}/status`: Atualiza o status operacional do pedido (`EM_PREPARO`, `PRONTO`, `ENTREGUE`, `CANCELADO`).