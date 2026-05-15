from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from database.settings import engine
from routes.routes import router

app = FastAPI(
    title="SIGEA - Sistema Integrado de Gestão de Espaços Acadêmicos",
    description="API para gerenciamento de salas e espaços acadêmicos",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception as exc:
        raise RuntimeError("Falha ao conectar ao MySQL local. Verifique as credenciais e o banco de dados.") from exc

app.include_router(router, prefix="/api", tags=["Recursos"])


@app.get("/")
async def root():
    """Rota raiz da API"""
    return {
        "message": "Bem-vindo ao SIGEA",
        "version": "0.1.0"
    }


@app.get("/health")
async def health_check():
    """Verificar saúde da API"""
    return {
        "status": "online"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
