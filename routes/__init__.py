from .auth import router as auth_router
from .reservas import router as reservas_router
from .usuarios import router as usuarios_router
from .eventos import router as eventos_router

sistema_router = auth_router
router_usuarios = usuarios_router

routers = [auth_router, reservas_router, usuarios_router, eventos_router]
