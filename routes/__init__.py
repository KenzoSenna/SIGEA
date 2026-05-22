from .auth import router as auth_router
from .reservas import router as reservas_router
from .usuarios import router as usuarios_router

# nomes de roteadores para inclusão no FastAPI app
sistema_router = auth_router
router_usuarios = usuarios_router

# lista de routers para inclusão no FastAPI app
routers = [auth_router, reservas_router, usuarios_router ]
