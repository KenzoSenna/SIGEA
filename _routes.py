# compact shim for reexporting routers with expected names

from routes import routers as _routers

# Reexport default names expected elsewhere
router = _routers[0]
router_usuarios = _routers[2]