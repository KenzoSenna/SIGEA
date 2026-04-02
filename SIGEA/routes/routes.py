from fastapi import APIRouter

router = APIRouter()
# Parte da auth
@router.post("/auth/login")
async def login():
    return {
        "email": "usuario@email.com",
        "sessao": "autenticada"
    }

# Parte dos users

@router.post("/usuarios")
async def create_usuario():
    return {
        "usuario": {
            "id": 1,
            "nome": "Nome",
            "email": "email@email.com",
            "tipo": "professor"
        }
    }

@router.get("/usuarios")
async def list_usuarios():
    return {
        "usuarios": [
            {
                "id": 1,
                "nome": "Nome",
                "email": "email@email.com",
                "tipo": "professor"
            }
        ]
    }

@router.get("/usuarios/{usuario_id}")
async def get_usuario(usuario_id: int):
    return {
        "usuario": {
            "id": usuario_id,
            "nome": "Nome",
            "email": "email@email.com",
            "tipo": "professor"
        }
    }

@router.put("/usuarios/{usuario_id}")
async def update_usuario(usuario_id: int):
    return {
        "usuario": {
            "id": usuario_id,
            "tipo": "admin"
        }
    }

@router.delete("/usuarios/{usuario_id}")
async def delete_usuario(usuario_id: int):
    return {
        "resultado": "removido"
    }

@router.post("/andares")
async def create_andar():
    return {
        "andar": {
            "id": 1,
            "numero": 1
        }
    }

# Parte dos andares

@router.get("/andares")
async def list_andares():
    return {
        "andares": [
            {
                "id": 1,
                "numero": 1
            }
        ]
    }

@router.get("/andares/{andar_id}")
async def get_andar(andar_id: int):
    return {
        "andar": {
            "id": andar_id,
            "numero": 1
        }
    }

@router.put("/andares/{andar_id}")
async def update_andar(andar_id: int):
    return {
        "andar": {
            "id": andar_id,
            "numero": 2
        }
    }

@router.delete("/andares/{andar_id}")
async def delete_andar(andar_id: int):
    return {
        "resultado": "removido"
    }

# Parte das salas

@router.post("/salas")
async def create_sala():
    return {
        "sala": {
            "id": 1,
            "nome": "Sala 1",
            "capacidade": 30,
            "tipo": "sala",
            "id_andar": 1
        }
    }

@router.get("/salas")
async def list_salas():
    return {
        "salas": [
            {
                "id": 1,
                "nome": "Sala 1",
                "capacidade": 30,
                "tipo": "sala",
                "id_andar": 1
            }
        ]
    }

@router.get("/salas/{sala_id}")
async def get_sala(sala_id: int):
    return {
        "sala": {
            "id": sala_id,
            "nome": "Sala 1",
            "capacidade": 30,
            "tipo": "sala",
            "id_andar": 1
        }
    }

@router.put("/salas/{sala_id}")
async def update_sala(sala_id: int):
    return {
        "sala": {
            "id": sala_id,
            "nome": "Sala Atualizada",
            "capacidade": 35,
            "tipo": "sala",
            "id_andar": 1
        }
    }

@router.delete("/salas/{sala_id}")
async def delete_sala(sala_id: int):
    return {
        "resultado": "removido"
    }

@router.post("/salas/{sala_id}/horarios")
async def definir_horarios_sala(sala_id: int):
    return {
        "id_sala": sala_id,
        "horarios": [
            {
                "inicio": "08:00",
                "fim": "10:00"
            }
        ]
    }

@router.get("/salas/status")
async def status_salas():
    return {
        "salas": [
            {
                "id_sala": 1,
                "status": "ocupada"
            }
        ]
    }

@router.get("/salas/busca")
async def buscar_salas():
    return {
        "salas": [
            {
                "id": 1,
                "nome": "Sala 1",
                "capacidade": 30,
                "tipo": "sala",
                "id_andar": 1
            }
        ]
    }

@router.get("/salas/{sala_id}/localizacao")
async def localizar_sala(sala_id: int):
    return {
        "id_sala": sala_id,
        "andar": 1
    }

# Parte das disciplinas

@router.post("/disciplinas")
async def create_disciplina():
    return {
        "disciplina": {
            "id": 1,
            "nome": "Disciplina",
            "codigo": "COD01"
        }
    }

@router.get("/disciplinas")
async def list_disciplinas():
    return {
        "disciplinas": [
            {
                "id": 1,
                "nome": "Disciplina",
                "codigo": "COD01"
            }
        ]
    }

@router.get("/disciplinas/{disciplina_id}")
async def get_disciplina(disciplina_id: int):
    return {
        "disciplina": {
            "id": disciplina_id,
            "nome": "Disciplina",
            "codigo": "COD01"
        }
    }

@router.put("/disciplinas/{disciplina_id}")
async def update_disciplina(disciplina_id: int):
    return {
        "disciplina": {
            "id": disciplina_id,
            "nome": "Disciplina Atualizada",
            "codigo": "COD01"
        }
    }

@router.delete("/disciplinas/{disciplina_id}")
async def delete_disciplina(disciplina_id: int):
    return {
        "resultado": "removido"
    }

@router.post("/usuarios/{usuario_id}/disciplinas/{disciplina_id}")
async def associar_usuario_disciplina(usuario_id: int, disciplina_id: int):
    return {
        "id_usuario": usuario_id,
        "id_disciplina": disciplina_id
    }

@router.delete("/usuarios/{usuario_id}/disciplinas/{disciplina_id}")
async def remover_usuario_disciplina(usuario_id: int, disciplina_id: int):
    return {
        "resultado": "removido"
    }

# Parte das reservas

@router.post("/reservas")
async def create_reserva():
    return {
        "reserva": {
            "id": 1,
            "id_sala": 1,
            "id_disciplina": 1,
            "data_inicio": "2026-04-10 08:00",
            "data_fim": "2026-04-10 10:00",
            "descricao": "Aula"
        }
    }

@router.get("/reservas")
async def list_reservas():
    return {
        "reservas": [
            {
                "id": 1,
                "id_sala": 1,
                "id_disciplina": 1,
                "data_inicio": "2026-04-10 08:00",
                "data_fim": "2026-04-10 10:00",
                "descricao": "Aula"
            }
        ]
    }

@router.get("/reservas/{reserva_id}")
async def get_reserva(reserva_id: int):
    return {
        "reserva": {
            "id": reserva_id,
            "id_sala": 1,
            "id_disciplina": 1,
            "data_inicio": "2026-04-10 08:00",
            "data_fim": "2026-04-10 10:00",
            "descricao": "Aula"
        }
    }

@router.delete("/reservas/{reserva_id}")
async def cancelar_reserva(reserva_id: int):
    return {
        "id_reserva": reserva_id,
        "status": "cancelada"
    }

@router.post("/reservas/validar-conflito")
async def validar_conflito():
    return {
        "valido": True
    }

@router.get("/reservas/disponibilidade")
async def consultar_disponibilidade():
    return {
        "salas": [
            {
                "id_sala": 1,
                "disponivel": True
            }
        ]
    }

# Parte dos eventos

@router.post("/eventos")
async def create_evento():
    return {
        "evento": {
            "id": 1,
            "titulo": "Evento",
            "descricao": "Descricao",
            "id_sala": 1,
            "data_inicio": "2026-05-01 08:00",
            "data_fim": "2026-05-01 10:00",
            "tipo": "institucional"
        }
    }

@router.get("/eventos")
async def list_eventos():
    return {
        "eventos": [
            {
                "id": 1,
                "titulo": "Evento",
                "descricao": "Descricao",
                "id_sala": 1,
                "data_inicio": "2026-05-01 08:00",
                "data_fim": "2026-05-01 10:00",
                "tipo": "institucional"
            }
        ]
    }

@router.get("/eventos/{evento_id}")
async def get_evento(evento_id: int):
    return {
        "evento": {
            "id": evento_id,
            "titulo": "Evento",
            "descricao": "Descricao",
            "id_sala": 1,
            "data_inicio": "2026-05-01 08:00",
            "data_fim": "2026-05-01 10:00",
            "tipo": "institucional"
        }
    }

@router.put("/eventos/{evento_id}")
async def update_evento(evento_id: int):
    return {
        "evento": {
            "id": evento_id,
            "titulo": "Evento Atualizado",
            "descricao": "Descricao",
            "id_sala": 1,
            "data_inicio": "2026-05-01 08:00",
            "data_fim": "2026-05-01 10:00",
            "tipo": "institucional"
        }
    }

@router.delete("/eventos/{evento_id}")
async def delete_evento(evento_id: int):
    return {
        "resultado": "removido"
    }

@router.post("/eventos/{evento_id}/participar")
async def participar_evento(evento_id: int):
    return {
        "id_evento": evento_id,
        "participacao": "confirmada"
    }

@router.delete("/eventos/{evento_id}/participar")
async def sair_evento(evento_id: int):
    return {
        "id_evento": evento_id,
        "participacao": "removida"
    }

# Parte da agenda

@router.get("/usuarios/{usuario_id}/agenda")
async def agenda_usuario(usuario_id: int):
    return {
        "id_usuario": usuario_id,
        "reservas": [
            {
                "id": 1,
                "id_sala": 1,
                "data_inicio": "2026-04-10 08:00",
                "data_fim": "2026-04-10 10:00"
            }
        ],
        "eventos": [
            {
                "id": 1,
                "titulo": "Evento",
                "data_inicio": "2026-05-01 08:00",
                "data_fim": "2026-05-01 10:00"
            }
        ]
    }

@router.get("/agenda")
async def agenda_geral():
    return {
        "data": "2026-04-10",
        "reservas": [
            {
                "id": 1,
                "id_sala": 1,
                "data_inicio": "2026-04-10 08:00",
                "data_fim": "2026-04-10 10:00"
            }
        ],
        "eventos": [
            {
                "id": 1,
                "titulo": "Evento",
                "data_inicio": "2026-05-01 08:00",
                "data_fim": "2026-05-01 10:00"
            }
        ]
    }