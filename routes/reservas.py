from fastapi import APIRouter, Depends, HTTPException
from routes.schemas import ReservaRequest
from routes import store
from utils import validate_user_role

router = APIRouter(tags=["Reservas"])

@router.post("/reservas", summary="Realizar reserva de sala")
async def create_reserva(dados: ReservaRequest, current_user: dict = Depends(store.get_current_user)):
    global store
    if dados.id_sala not in store.SALAS:
        raise HTTPException(status_code=404, detail={"sucesso": False, "mensagem": "Sala não encontrada"})
    
    if store._verificar_conflito(dados.id_sala, dados.detalhes, dados.tipo_reserva):
        raise HTTPException(status_code=409, detail={"sucesso": False, "mensagem": "Horário indisponível nesta sala"})
    
    store.contador_reserva += 1
    id_reserva = store.contador_reserva
    
    if dados.tipo_reserva == "diaria":
        store.reservas[id_reserva] = {
            "id_sala": dados.id_sala,
            "id_disciplina": dados.id_disciplina,
            "descricao": dados.descricao,
            "tipo_reserva": dados.tipo_reserva,
            "data": str(dados.detalhes.data),
            "horario_inicio": str(dados.detalhes.horario_inicio),
            "horario_fim": str(dados.detalhes.horario_fim),
        }
    elif dados.tipo_reserva == "semestral":
        store.reservas[id_reserva] = {
            "id_sala": dados.id_sala,
            "id_disciplina": dados.id_disciplina,
            "descricao": dados.descricao,
            "tipo_reserva": dados.tipo_reserva,
            "data_inicio": str(dados.detalhes.data_inicio),
            "data_fim": str(dados.detalhes.data_fim),
            "dias_semana": dados.detalhes.dias_semana,
            "horarios": {dia: {"inicio": str(h["inicio"]), "fim": str(h["fim"])} 
                        for dia, h in dados.detalhes.horarios.items()},
        }

    return {
        "sucesso": True, 
        "mensagem": f"Reserva {dados.tipo_reserva} realizada com sucesso!",
        "id_reserva": id_reserva,
        "reserva": store.reservas[id_reserva]
    }

@router.get("/reservas", summary="Listar todas as reservas")
async def listar_reservas(current_user: dict = Depends(store.get_current_user)):
    return {
        "sucesso": True,
        "total": len(store.reservas),
        "reservas": store.reservas
    }

@router.get("/reservas/{id_reserva}", summary="Obter detalhes de uma reserva")
async def obter_reserva(id_reserva: int, current_user: dict = Depends(store.get_current_user)):
    if id_reserva not in store.reservas:
        raise HTTPException(status_code=404, detail={"sucesso": False, "mensagem": "Reserva não encontrada"})
    return {
        "sucesso": True,
        "reserva": store.reservas[id_reserva]
    }

@router.delete("/reservas/{id_reserva}", summary="Cancelar uma reserva")
async def cancelar_reserva(id_reserva: int, current_user: dict = Depends(store.get_current_user)):
    if id_reserva not in store.reservas:
        raise HTTPException(status_code=404, detail={"sucesso": False, "mensagem": "Reserva não encontrada"})
    
    reserva_removida = store.reservas.pop(id_reserva)
    return {
        "sucesso": True,
        "mensagem": "Reserva cancelada com sucesso",
        "reserva_removida": reserva_removida
    }
