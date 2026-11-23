
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from api.pedido_controller import router as pedido_router
from infrastructure.database import initialize_database
from api.auth_controller import router as auth_router
from api.usuario_controller import router as usuario_router


app = FastAPI(
    title="API - Raízes do Nordeste",
    description="Sistema Back-End de Gerenciamento de Pedidos e Estoque - Rede Raízes do Nordeste",
    version="1.0.0"
)

@app.on_event("startup")
def startup():
    initialize_database()

@app.get("/", tags=["Sistema"])
def health_check():
    return {"status": "API Raízes do Nordeste online e operante."}

app.include_router(pedido_router)
app.include_router(auth_router)
app.include_router(usuario_router)
