
from .auth import router as auth_router
from .reservas import router as reservas_router
from .usuarios import router as usuarios_router
from .andares import router as andares_router
from .agendas import router as agendas_router

# nomes de roteadores para inclusão no FastAPI app
sistema_router = auth_router
router_usuarios = usuarios_router

# lista de routers para inclusão no FastAPI app
routers = [auth_router, reservas_router, usuarios_router, andares_router, agendas_router]
