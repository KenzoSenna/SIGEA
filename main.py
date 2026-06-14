import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from database.settings import engine, init_db, SessionLocal, settings
from routes import routers as api_routers
from services.manutencao import seed_default_user, purge_expired_tokens

logger = logging.getLogger("sigea")
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        init_db()

        db = SessionLocal()
        try:
            seed_default_user(db)
            removidos = purge_expired_tokens(db)
            if removidos:
                logger.info("Removidos %d tokens revogados já expirados", removidos)
        finally:
            db.close()
    except Exception as exc:
        raise RuntimeError("Falha ao conectar ao MySQL local. Verifique as credenciais e o banco de dados.") from exc

    if settings.secret_key_is_default:
        logger.warning(
            "SECRET_KEY padrão em uso — defina SECRET_KEY no .env antes de ir para produção."
        )

    yield


app = FastAPI(
    title="SIGEA - Sistema Integrado de Gestão de Espaços Acadêmicos",
    description="API para gerenciamento de salas e espaços acadêmicos",
    version="0.1.0",
    lifespan=lifespan,
)

# Autenticação usa header Authorization (Bearer), não cookies — credenciais
# de CORS ficam desabilitadas quando a origem é curinga.
cors_origins = settings.cors_origins_list
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials="*" not in cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    detail = exc.detail
    content = detail if isinstance(detail, dict) else {"sucesso": False, "mensagem": str(detail)}
    return JSONResponse(
        status_code=exc.status_code,
        headers=getattr(exc, "headers", None),
        content=content,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    erros = []
    for error in exc.errors():
        loc = [str(l) for l in error["loc"] if l not in ("body", "query", "path", "header")]
        campo = ".".join(loc) if loc else None
        msg = error["msg"].replace("Value error, ", "")
        erros.append(f"'{campo}': {msg}" if campo else msg)
    return JSONResponse(
        status_code=422,
        content={
            "sucesso": False,
            "mensagem": "Dados de entrada inválidos",
            "erros": erros,
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Erro não tratado em %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"sucesso": False, "mensagem": "Erro interno do servidor"},
    )


for r in api_routers:
    app.include_router(r)


@app.get("/")
async def root():
    return {
        "message": "Bem-vindo ao SIGEA",
        "version": "0.1.0"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "online"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
