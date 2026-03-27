from fastapi import APIRouter

router = APIRouter()

@router.post("/auth/login")  # RF02
async def login():
    pass

@router.post("/usuarios")  # RF01
async def create_usuario():
    pass

@router.get("/usuarios")
async def list_usuarios():
    pass

@router.get("/usuarios/{usuario_id}")
async def get_usuario(usuario_id: int):
    pass

@router.put("/usuarios/{usuario_id}")  # RF03 (gerenciamento de perfil)
async def update_usuario(usuario_id: int):
    pass

@router.delete("/usuarios/{usuario_id}")
async def delete_usuario(usuario_id: int):
    pass

@router.post("/andares")
async def create_andar():
    pass

@router.get("/andares")
async def list_andares():
    pass

@router.get("/andares/{andar_id}")
async def get_andar(andar_id: int):
    pass

@router.put("/andares/{andar_id}")
async def update_andar(andar_id: int):
    pass

@router.delete("/andares/{andar_id}")
async def delete_andar(andar_id: int):
    pass

@router.post("/salas")  # RF05
async def create_sala():
    pass

@router.get("/salas")
async def list_salas():
    pass

@router.get("/salas/{sala_id}")
async def get_sala(sala_id: int):
    pass

@router.put("/salas/{sala_id}")
async def update_sala(sala_id: int):
    pass

@router.delete("/salas/{sala_id}")
async def delete_sala(sala_id: int):
    pass

# RF06 - definir horários de alocação
@router.post("/salas/{sala_id}/horarios")
async def definir_horarios_sala(sala_id: int):
    pass

# RF12 - status das salas
@router.get("/salas/status")
async def status_salas():
    pass

# RF18 - filtros e busca
@router.get("/salas/busca")
async def buscar_salas():
    pass

# RF19 - localização
@router.get("/salas/{sala_id}/localizacao")
async def localizar_sala(sala_id: int):
    pass

@router.post("/disciplinas")  # RF07
async def create_disciplina():
    pass

@router.get("/disciplinas")
async def list_disciplinas():
    pass

@router.get("/disciplinas/{disciplina_id}")
async def get_disciplina(disciplina_id: int):
    pass

@router.put("/disciplinas/{disciplina_id}")
async def update_disciplina(disciplina_id: int):
    pass

@router.delete("/disciplinas/{disciplina_id}")
async def delete_disciplina(disciplina_id: int):
    pass

# RF08 - associação usuário-disciplina
@router.post("/usuarios/{usuario_id}/disciplinas/{disciplina_id}")
async def associar_usuario_disciplina(usuario_id: int, disciplina_id: int):
    pass

@router.delete("/usuarios/{usuario_id}/disciplinas/{disciplina_id}")
async def remover_usuario_disciplina(usuario_id: int, disciplina_id: int):
    pass

@router.post("/reservas")  # RF09
async def create_reserva():
    pass

@router.get("/reservas")
async def list_reservas():
    pass

@router.get("/reservas/{reserva_id}")
async def get_reserva(reserva_id: int):
    pass

@router.delete("/reservas/{reserva_id}")  # RF14
async def cancelar_reserva(reserva_id: int):
    pass

# RF10 - validação de conflito
@router.post("/reservas/validar-conflito")
async def validar_conflito():
    pass

# RF11 - disponibilidade de salas
@router.get("/reservas/disponibilidade")
async def consultar_disponibilidade():
    pass

@router.post("/eventos")  # RF15
async def create_evento():
    pass

@router.get("/eventos")  # RF16
async def list_eventos():
    pass

@router.get("/eventos/{evento_id}")
async def get_evento(evento_id: int):
    pass

@router.put("/eventos/{evento_id}")
async def update_evento(evento_id: int):
    pass

@router.delete("/eventos/{evento_id}")
async def delete_evento(evento_id: int):
    pass

# RF17 - participação
@router.post("/eventos/{evento_id}/participar")
async def participar_evento(evento_id: int):
    pass

@router.delete("/eventos/{evento_id}/participar")
async def sair_evento(evento_id: int):
    pass

# =========================

# RF13 - agenda do usuário
@router.get("/usuarios/{usuario_id}/agenda")
async def agenda_usuario(usuario_id: int):
    pass

# RF20 - agenda geral
@router.get("/agenda")
async def agenda_geral():
    pass