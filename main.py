from fastapi import FastAPI
from api.pedido_controller import router as pedido_router

app = FastAPI(
    title="API - Raízes do Nordeste",
    description="Sistema Back-End de Gerenciamento de Pedidos e Estoque - Rede Raízes do Nordeste",
    version="1.0.0"
)

@app.get("/", tags=["Sistema"])
def health_check():
    return {"status": "API Raízes do Nordeste online e operante."}

app.include_router(pedido_router)