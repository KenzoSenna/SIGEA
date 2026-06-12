from .auth import router as auth_router
from .reservas import router as reservas_router
from .usuarios import router as usuarios_router
from .eventos import router as eventos_router
from .andares import router as andares_router
from .salas import router as salas_router

routers = [auth_router, usuarios_router, andares_router, salas_router, eventos_router, reservas_router]
